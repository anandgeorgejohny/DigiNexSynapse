/**
 * DigiNexSynapse - App1: Dynamic API Router
 * Kiroween 2026 Hackathon: Skeleton Crew Category
 *
 * Simulates receiving incoming API payloads and intelligently routing them
 * through a mock Kiro Model Context Protocol (MCP) agent framework.
 */

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

// Safe environment loading
try {
  require('dotenv').config();
} catch (e) {
  // Graceful fallback if dependencies are not yet installed
}

const PORT = process.env.PORT || 3000;
const STEERING_FILE = path.resolve(__dirname, '../.kiro/steering.md');

// Load steering configuration to ground agent behavior
let steeringInstruction = 'Default: Operate deterministically.';
if (fs.existsSync(STEERING_FILE)) {
  steeringInstruction = fs.readFileSync(STEERING_FILE, 'utf8').trim();
}

/**
 * Mock Kiro MCP Agent Catalog
 */
const MCP_AGENT_REGISTRY = {
  'telemetry.analyze': {
    agentId: 'agent-telemetry-01',
    capabilities: ['metrics_parsing', 'anomaly_detection'],
    targetSubsystem: 'monitoring-gateway'
  },
  'incident.resolve': {
    agentId: 'agent-incident-resolver-02',
    capabilities: ['log_retrieval', 'similarity_search', 'remediation'],
    targetSubsystem: 'App2-Incident-Resolver'
  },
  'traffic.throttle': {
    agentId: 'agent-load-balancer-03',
    capabilities: ['rate_limiting', 'circuit_breaker'],
    targetSubsystem: 'edge-proxy'
  }
};

/**
 * Mock Kiro MCP Routing Engine
 */
function routeViaKiroMCP(payload) {
  const { eventType, severity, source, metadata } = payload;
  console.log(`\n[Kiro MCP Router] Evaluating payload from source [${source || 'unknown'}]...`);
  console.log(`[Kiro MCP Router] Applying steering rules: "${steeringInstruction.slice(0, 80)}..."`);

  // Rule-based deterministic routing with MCP dispatch
  let matchedRoute = MCP_AGENT_REGISTRY[eventType];

  if (!matchedRoute) {
    if (severity === 'CRITICAL' || severity === 'HIGH') {
      matchedRoute = MCP_AGENT_REGISTRY['incident.resolve'];
    } else {
      matchedRoute = MCP_AGENT_REGISTRY['telemetry.analyze'];
    }
  }

  const dispatchPacket = {
    mcpVersion: '2026-11-kiro-draft',
    traceId: `trace-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
    timestamp: new Date().toISOString(),
    assignedAgent: matchedRoute.agentId,
    targetSubsystem: matchedRoute.targetSubsystem,
    action: eventType || 'generic.dispatch',
    payload: {
      ...payload,
      routedBy: 'DigiNexSynapse-Dynamic-API-Router'
    },
    steeringEnforced: true,
    status: 'ROUTED_SUCCESS'
  };

  return dispatchPacket;
}

// HTTP Server definition
const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  // Health check endpoint
  if (req.method === 'GET' && url.pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'UP', service: 'Dynamic-API-Router', timestamp: new Date().toISOString() }));
  }

  // MCP Routing endpoint
  if (req.method === 'POST' && url.pathname === '/api/route') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const payload = JSON.parse(body || '{}');
        const routedResult = routeViaKiroMCP(payload);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify(routedResult, null, 2));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({ error: 'Invalid JSON payload', details: err.message }));
      }
    });
    return;
  }

  // Root landing info
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({
    name: 'DigiNexSynapse Dynamic API Router',
    description: 'Autonomous Kiro MCP agent routing interface',
    endpoints: {
      'POST /api/route': 'Route payload through Kiro MCP agents',
      'GET /health': 'Service health status'
    }
  }, null, 2));
});

// Self-executing demo when run directly
if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`====================================================`);
    console.log(`🚀 DigiNexSynapse Dynamic API Router listening on port ${PORT}`);
    console.log(`📡 Ready for Kiro MCP Agent Payloads at http://localhost:${PORT}/api/route`);
    console.log(`====================================================`);

    // Simulate an autonomous routing event for verification
    const mockEvent = {
      eventType: 'incident.resolve',
      severity: 'CRITICAL',
      source: 'prod-cluster-east-node4',
      message: 'Connection pool exhausted; database timeout exceeded',
      metadata: { activeConnections: 1024, maxLimit: 1024 }
    };
    
    console.log('\n[Demo Mode] Dispatching simulated test payload...');
    const demoResult = routeViaKiroMCP(mockEvent);
    console.log('[Demo Mode] Result:\n', JSON.stringify(demoResult, null, 2));
  });
}

module.exports = { server, routeViaKiroMCP };
