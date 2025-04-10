import { Node, Edge, MarkerType, Position } from 'reactflow';

// Create a new flowchart with improved default structure
export function createNewFlowchart(): { nodes: Node[], edges: Edge[] } {
  return {
    nodes: [
      {
        id: '1',
        type: 'terminal',
        data: { label: 'Start', color: '#90EE90' },
        position: { x: 250, y: 0 },
      },
      {
        id: '2',
        type: 'process',
        data: { label: 'Process Step', color: '#ADD8E6' },
        position: { x: 250, y: 100 },
      },
      {
        id: '3',
        type: 'decision',
        data: { label: 'Decision?', color: '#FFFACD' },
        position: { x: 250, y: 200 },
      },
      {
        id: '4',
        type: 'process',
        data: { label: 'Yes Path', color: '#ADD8E6' },
        position: { x: 100, y: 300 },
      },
      {
        id: '5',
        type: 'process',
        data: { label: 'No Path', color: '#ADD8E6' },
        position: { x: 400, y: 300 },
      },
      {
        id: '6',
        type: 'terminal',
        data: { label: 'End', color: '#FFB6C1' },
        position: { x: 250, y: 400 },
      },
    ],
    edges: [
      { 
        id: 'e1-2', 
        source: '1', 
        target: '2', 
        animated: false,
        markerEnd: { type: MarkerType.ArrowClosed }
      },
      {
        id: 'e2-3', 
        source: '2', 
        target: '3', 
        animated: false,
        markerEnd: { type: MarkerType.ArrowClosed }
      },
      {
        id: 'e3-4', 
        source: '3', 
        target: '4', 
        label: 'Yes',
        animated: false,
        sourceHandle: 'left',
        markerEnd: { type: MarkerType.ArrowClosed }
      },
      {
        id: 'e3-5', 
        source: '3', 
        target: '5', 
        label: 'No',
        animated: false,
        sourceHandle: 'right',
        markerEnd: { type: MarkerType.ArrowClosed }
      },
      {
        id: 'e4-6', 
        source: '4', 
        target: '6', 
        animated: false,
        markerEnd: { type: MarkerType.ArrowClosed }
      },
      {
        id: 'e5-6', 
        source: '5', 
        target: '6', 
        animated: false,
        markerEnd: { type: MarkerType.ArrowClosed }
      },
    ],
  };
}

// Add a node to the flowchart
export function addNode(
  nodes: Node[],
  edges: Edge[],
  nodeType: string = 'default',
  label: string = 'New Node',
  position: { x: number, y: number } = { x: 250, y: 300 }
): { nodes: Node[], edges: Edge[] } {
  const newId = `node_${Date.now()}`;
  const newNode: Node = {
    id: newId,
    type: nodeType,
    data: { label },
    position,
  };

  return {
    nodes: [...nodes, newNode],
    edges,
  };
}

// Remove a node from the flowchart
export function removeNode(
  nodes: Node[],
  edges: Edge[],
  nodeId: string
): { nodes: Node[], edges: Edge[] } {
  const updatedNodes = nodes.filter(node => node.id !== nodeId);
  const updatedEdges = edges.filter(
    edge => edge.source !== nodeId && edge.target !== nodeId
  );

  return {
    nodes: updatedNodes,
    edges: updatedEdges,
  };
}

// Add an edge between two nodes
export function addEdge(
  nodes: Node[],
  edges: Edge[],
  source: string,
  target: string,
  label?: string
): { nodes: Node[], edges: Edge[] } {
  const newEdge: Edge = {
    id: `e${source}-${target}`,
    source,
    target,
    label,
    animated: false,
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  };

  return {
    nodes,
    edges: [...edges, newEdge],
  };
}

// Remove an edge
export function removeEdge(
  nodes: Node[],
  edges: Edge[],
  edgeId: string
): { nodes: Node[], edges: Edge[] } {
  return {
    nodes,
    edges: edges.filter(edge => edge.id !== edgeId),
  };
}

// Update a node's properties
export function updateNode(
  nodes: Node[],
  edges: Edge[],
  nodeId: string,
  updates: Partial<Node>
): { nodes: Node[], edges: Edge[] } {
  const updatedNodes = nodes.map(node => {
    if (node.id === nodeId) {
      // Handle specific updates for data.label separately
      if (updates.data && 'label' in updates.data) {
        return {
          ...node,
          ...updates,
          data: {
            ...node.data,
            label: updates.data.label,
          },
        };
      }
      return { ...node, ...updates };
    }
    return node;
  });

  return {
    nodes: updatedNodes,
    edges,
  };
}

// Update an edge's properties
export function updateEdge(
  nodes: Node[],
  edges: Edge[],
  edgeId: string,
  updates: Partial<Edge>
): { nodes: Node[], edges: Edge[] } {
  const updatedEdges = edges.map(edge => {
    if (edge.id === edgeId) {
      return { ...edge, ...updates };
    }
    return edge;
  });

  return {
    nodes,
    edges: updatedEdges,
  };
}

// Create decision tree structure with proper node types
export function createDecisionTree(): { nodes: Node[], edges: Edge[] } {
  return {
    nodes: [
      { id: '1', type: 'terminal', data: { label: 'Start', color: '#90EE90' }, position: { x: 250, y: 0 } },
      { id: '2', type: 'decision', data: { label: 'Decision Point 1', color: '#FFFACD' }, position: { x: 250, y: 100 } },
      { id: '3', type: 'process', data: { label: 'Option A', color: '#ADD8E6' }, position: { x: 100, y: 200 } },
      { id: '4', type: 'process', data: { label: 'Option B', color: '#ADD8E6' }, position: { x: 400, y: 200 } },
      { id: '5', type: 'decision', data: { label: 'Decision Point 2', color: '#FFFACD' }, position: { x: 100, y: 300 } },
      { id: '6', type: 'process', data: { label: 'Option C', color: '#ADD8E6' }, position: { x: 0, y: 400 } },
      { id: '7', type: 'process', data: { label: 'Option D', color: '#ADD8E6' }, position: { x: 200, y: 400 } },
      { id: '8', type: 'terminal', data: { label: 'End', color: '#FFB6C1' }, position: { x: 250, y: 500 } }
    ],
    edges: [
      { id: 'e1-2', source: '1', target: '2', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e2-3', source: '2', target: '3', label: 'Yes', sourceHandle: 'left', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e2-4', source: '2', target: '4', label: 'No', sourceHandle: 'right', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e3-5', source: '3', target: '5', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e5-6', source: '5', target: '6', label: 'Yes', sourceHandle: 'left', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e5-7', source: '5', target: '7', label: 'No', sourceHandle: 'right', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e4-8', source: '4', target: '8', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e6-8', source: '6', target: '8', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e7-8', source: '7', target: '8', animated: false, markerEnd: { type: MarkerType.ArrowClosed } }
    ]
  };
}

// Create process flowchart structure with proper node types
export function createProcessFlowchart(): { nodes: Node[], edges: Edge[] } {
  return {
    nodes: [
      { id: '1', type: 'terminal', data: { label: 'Start', color: '#90EE90' }, position: { x: 250, y: 0 } },
      { id: '2', type: 'input', data: { label: 'Get User Input', color: '#F0E68C' }, position: { x: 250, y: 100 } },
      { id: '3', type: 'process', data: { label: 'Process Data', color: '#ADD8E6' }, position: { x: 250, y: 200 } },
      { id: '4', type: 'decision', data: { label: 'Valid Data?', color: '#FFFACD' }, position: { x: 250, y: 300 } },
      { id: '5', type: 'process', data: { label: 'Handle Error', color: '#FFB6C1' }, position: { x: 450, y: 400 } },
      { id: '6', type: 'output', data: { label: 'Display Results', color: '#D8BFD8' }, position: { x: 250, y: 400 } },
      { id: '7', type: 'terminal', data: { label: 'End', color: '#FFB6C1' }, position: { x: 250, y: 500 } },
    ],
    edges: [
      { id: 'e1-2', source: '1', target: '2', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e2-3', source: '2', target: '3', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e3-4', source: '3', target: '4', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e4-5', source: '4', target: '5', label: 'No', sourceHandle: 'right', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e4-6', source: '4', target: '6', label: 'Yes', sourceHandle: 'left', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e5-2', source: '5', target: '2', animated: false, markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e6-7', source: '6', target: '7', animated: false, markerEnd: { type: MarkerType.ArrowClosed } }
    ]
  };
}

// Apply a hierarchical auto-layout to the flowchart that resembles the examples
export function applyAutoLayout(nodes: Node[], edges: Edge[]): { nodes: Node[], edges: Edge[] } {
  // Don't modify if no nodes
  if (nodes.length === 0) return { nodes, edges };
  
  const nodeMap = new Map(nodes.map(node => [node.id, node]));
  const edgeMap = new Map<string, Edge[]>();
  
  // Build edge mappings by source
  edges.forEach(edge => {
    if (!edgeMap.has(edge.source)) {
      edgeMap.set(edge.source, []);
    }
    edgeMap.get(edge.source)?.push(edge);
  });
  
  // Build edge mappings by target
  const targetEdgeMap = new Map<string, Edge[]>();
  edges.forEach(edge => {
    if (!targetEdgeMap.has(edge.target)) {
      targetEdgeMap.set(edge.target, []);
    }
    targetEdgeMap.get(edge.target)?.push(edge);
  });
  
  // Find root nodes (nodes without incoming edges)
  const rootNodes = nodes.filter(node => !targetEdgeMap.has(node.id) || targetEdgeMap.get(node.id)?.length === 0);
  
  // Default to first node if no root found
  if (rootNodes.length === 0 && nodes.length > 0) {
    rootNodes.push(nodes[0]);
  }
  
  // Create levelMap to store each node's level in the hierarchy
  const levelMap = new Map<string, number>();
  const processedNodes = new Set<string>();
  
  // Track branches for decision nodes
  const decisionBranches = new Map<string, { 
    yesNode: string | null, 
    noNode: string | null,
    mergePoint: string | null 
  }>();
  
  // Calculate levels using BFS
  const queue: { nodeId: string, level: number, branchType?: string, parentDecision?: string }[] = [];
  rootNodes.forEach(node => {
    queue.push({ nodeId: node.id, level: 0 });
    levelMap.set(node.id, 0);
    processedNodes.add(node.id);
  });
  
  while (queue.length > 0) {
    const { nodeId, level, branchType, parentDecision } = queue.shift()!;
    const node = nodeMap.get(nodeId);
    
    // Process all outgoing edges
    const outgoingEdges = edgeMap.get(nodeId) || [];
    
    // For decision nodes, we need special handling
    if (node && (node.type === 'decision' || String(nodeId).includes('decision'))) {
      // Track this decision node's branches
      decisionBranches.set(nodeId, { 
        yesNode: null, 
        noNode: null,
        mergePoint: null
      });
      
      // Find Yes and No branches
      let yesEdge = outgoingEdges.find(e => e.label === 'Yes');
      let noEdge = outgoingEdges.find(e => e.label === 'No');
      
      // If not labeled, use the first two edges
      if (!yesEdge && !noEdge && outgoingEdges.length >= 2) {
        yesEdge = outgoingEdges[0];
        noEdge = outgoingEdges[1];
      }
      
      if (yesEdge) {
        const branchInfo = decisionBranches.get(nodeId);
        if (branchInfo) branchInfo.yesNode = yesEdge.target;
        
        // Process Yes branch with higher priority but same level
        if (!processedNodes.has(yesEdge.target)) {
          levelMap.set(yesEdge.target, level + 1);
          queue.push({ 
            nodeId: yesEdge.target, 
            level: level + 1,
            branchType: 'yes',
            parentDecision: nodeId 
          });
          processedNodes.add(yesEdge.target);
        }
      }
      
      if (noEdge) {
        const branchInfo = decisionBranches.get(nodeId);
        if (branchInfo) branchInfo.noNode = noEdge.target;
        
        // Process No branch
        if (!processedNodes.has(noEdge.target)) {
          levelMap.set(noEdge.target, level + 1);
          queue.push({ 
            nodeId: noEdge.target, 
            level: level + 1,
            branchType: 'no',
            parentDecision: nodeId 
          });
          processedNodes.add(noEdge.target);
        }
      }
      
      // Skip other edges for decision nodes as they should only have Yes/No
      continue;
    }
    
    // For normal nodes, process all outgoing edges
    outgoingEdges.forEach(edge => {
      // Skip if it's a Yes or No edge from a decision, as we handled those separately
      if (edge.label === 'Yes' || edge.label === 'No') {
        return;
      }
      
      // Add target node to next level if not processed
      if (!processedNodes.has(edge.target)) {
        // Special case: this might be a merge point for branches
        if (targetEdgeMap.get(edge.target)?.length && targetEdgeMap.get(edge.target)!.length > 1) {
          // Check if this is a merge point for a decision branch
          const incomingEdgeSources = targetEdgeMap.get(edge.target)!.map(e => e.source);
          
          // Check all decision branches to see if this is a merge point
          decisionBranches.forEach((branch, decisionId) => {
            if (branch.yesNode && branch.noNode) {
              // Check if the incoming edges include paths from both Yes and No branches
              const hasYesPath = incomingEdgeSources.includes(branch.yesNode);
              const hasNoPath = incomingEdgeSources.includes(branch.noNode);
              
              if (hasYesPath || hasNoPath) {
                branch.mergePoint = edge.target;
              }
            }
          });
        }
        
        levelMap.set(edge.target, level + 1);
        queue.push({ nodeId: edge.target, level: level + 1 });
        processedNodes.add(edge.target);
      }
    });
  }
  
  // Calculate actual positions with improved spacing
  const verticalSpacing = 150; // Space between levels
  const horizontalSpacing = 200; // Space between nodes in same level
  const decisionBranchSpacing = 150; // Horizontal distance for decision branches
  
  // Create a map of horizontal positions to avoid overlap
  const horizontalPositions = new Map<number, Set<number>>();
  
  // First, position the main flow (nodes not in decision branches)
  const mainFlow = new Set<string>();
  const branchFlow = new Map<string, { branchType: string, parentDecision: string }>();
  
  // Identify main flow vs branch flow nodes
  nodes.forEach(node => {
    const isInBranch = false; // Default assumption
    mainFlow.add(node.id);
  });
  
  decisionBranches.forEach((branch, decisionId) => {
    mainFlow.add(decisionId); // Decision node is part of main flow
    if (branch.mergePoint) mainFlow.add(branch.mergePoint); // Merge point is part of main flow
    
    // Yes and No branches are not part of main flow
    if (branch.yesNode) {
      mainFlow.delete(branch.yesNode);
      branchFlow.set(branch.yesNode, { branchType: 'yes', parentDecision: decisionId });
    }
    if (branch.noNode) {
      mainFlow.delete(branch.noNode);
      branchFlow.set(branch.noNode, { branchType: 'no', parentDecision: decisionId });
    }
  });
  
  // Map node levels to x positions for main flow (centered)
  const levelWidths = new Map<number, number>();
  const nodesAtLevel = new Map<number, string[]>();
  
  // Group nodes by level
  mainFlow.forEach(nodeId => {
    const level = levelMap.get(nodeId) || 0;
    if (!nodesAtLevel.has(level)) {
      nodesAtLevel.set(level, []);
    }
    nodesAtLevel.get(level)?.push(nodeId);
  });
  
  // Calculate positions for main flow nodes
  const updatedNodes = [...nodes];
  const centerX = 250; // Center x position
  
  // Position main flow nodes
  nodesAtLevel.forEach((nodeIds, level) => {
    const width = (nodeIds.length - 1) * horizontalSpacing;
    const startX = centerX - width / 2;
    
    nodeIds.forEach((nodeId, index) => {
      const node = nodeMap.get(nodeId);
      if (node) {
        const x = startX + index * horizontalSpacing;
        
        // Initialize or update the set of horizontal positions for this level
        if (!horizontalPositions.has(level)) {
          horizontalPositions.set(level, new Set<number>());
        }
        horizontalPositions.get(level)?.add(x);
        
        // Update node position
        node.position = {
          x: x,
          y: level * verticalSpacing
        };
      }
    });
  });
  
  // Now position branch nodes relative to their parent decision nodes
  branchFlow.forEach((branchInfo, nodeId) => {
    const node = nodeMap.get(nodeId);
    if (!node) return;
    
    const level = levelMap.get(nodeId) || 0;
    const parentDecision = nodeMap.get(branchInfo.parentDecision);
    
    if (parentDecision) {
      const parentX = parentDecision.position.x;
      const parentY = parentDecision.position.y;
      
      if (branchInfo.branchType === 'yes') {
        // Position Yes branch to the left
        node.position = {
          x: parentX - decisionBranchSpacing,
          y: parentY + verticalSpacing
        };
      } else if (branchInfo.branchType === 'no') {
        // Position No branch to the right
        node.position = {
          x: parentX + decisionBranchSpacing,
          y: parentY + verticalSpacing
        };
      }
      
      // Update the set of horizontal positions for this level
      if (!horizontalPositions.has(level)) {
        horizontalPositions.set(level, new Set<number>());
      }
      horizontalPositions.get(level)?.add(node.position.x);
    }
  });
  
  // Update edges for decision nodes to use proper handles and labels
  const updatedEdges = edges.map(edge => {
    const sourceNode = nodeMap.get(edge.source);
    const targetNode = nodeMap.get(edge.target);
    
    let updatedEdge = { ...edge, animated: false };
    
    // Set source/target handles based on relative positions
    if (sourceNode && targetNode) {
      const sourceType = sourceNode.type || '';
      
      // For decision nodes
      if (sourceType === 'decision' || sourceNode.id.includes('decision')) {
        if (targetNode.position.x < sourceNode.position.x) {
          // Left branch typically "Yes"
          updatedEdge = {
            ...updatedEdge,
            label: edge.label || 'Yes',
            sourceHandle: 'left'
          };
        } else if (targetNode.position.x > sourceNode.position.x) {
          // Right branch typically "No"
          updatedEdge = {
            ...updatedEdge,
            label: edge.label || 'No',
            sourceHandle: 'right'
          };
        }
      }
      
      // Add arrow markers to all edges
      updatedEdge = {
        ...updatedEdge,
        markerEnd: {
          type: MarkerType.ArrowClosed
        },
        style: { stroke: '#555', strokeWidth: 2 }
      };
    }
    
    return updatedEdge;
  });
  
  return {
    nodes: updatedNodes,
    edges: updatedEdges
  };
}

// Export to JSON
export function exportToJson(nodes: Node[], edges: Edge[]): string {
  return JSON.stringify({ nodes, edges }, null, 2);
}

// Import from JSON
export function importFromJson(jsonString: string): { nodes: Node[], edges: Edge[] } | null {
  try {
    const data = JSON.parse(jsonString);
    
    // Validate the structure
    if (!Array.isArray(data.nodes) || !Array.isArray(data.edges)) {
      return null;
    }
    
    return data;
  } catch (error) {
    console.error('Error parsing flowchart JSON:', error);
    return null;
  }
}
