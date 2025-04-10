import { Node, Edge } from 'reactflow';
import { MindMapNode, MindMapData } from '@/lib/mindmapUtils';

// Project types
export interface Project {
  id: number;
  userId?: number;
  name: string;
  type: 'mindmap' | 'flowchart';
  data: MindMapData | FlowchartData;
  thumbnail?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateProjectInput {
  name: string;
  type: 'mindmap' | 'flowchart';
  data: MindMapData | FlowchartData;
  userId?: number;
  thumbnail?: string;
}

export interface UpdateProjectInput {
  name?: string;
  data?: MindMapData | FlowchartData;
  thumbnail?: string;
}

// Template types
export interface Template {
  id: number;
  name: string;
  type: 'mindmap' | 'flowchart';
  data: MindMapData | FlowchartData;
  thumbnail?: string;
  description?: string;
}

// Mind Map types (re-exported for convenience)
export type { MindMapNode, MindMapData };

// Flowchart types
export interface FlowchartData {
  nodes: Node[];
  edges: Edge[];
}

// AI Generation types
export interface AIGenerationInput {
  type: 'mindmap' | 'flowchart';
  prompt: string;
  options?: {
    complexity?: 'simple' | 'medium' | 'complex' | 'comprehensive';
    style?: 'standard' | 'professional' | 'creative' | 'minimal';
  };
}

export interface AIGenerationResult {
  data: MindMapData | FlowchartData;
  error?: string;
}

// Export types
export interface ExportOptions {
  filename?: string;
  quality?: number;
  backgroundColor?: string;
  format: 'png' | 'svg' | 'pdf';
}

// User interface types
export interface NodeProperties {
  id: string;
  text: string;
  children: string[];
  color?: string;
  shape?: string;
  fontSize?: string;
  fontFamily?: string;
  connectorStyle?: string;
}
