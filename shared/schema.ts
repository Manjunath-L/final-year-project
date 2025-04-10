import { z } from "zod";

// Define diagram types
export const diagramTypeSchema = z.enum(['mindmap', 'flowchart']);
export type DiagramType = z.infer<typeof diagramTypeSchema>;

// Define types without database dependencies
export interface User {
  id: number;
  username: string;
  password: string;
}

export interface InsertUser {
  username: string;
  password: string;
}

export interface Project {
  id: number;
  userId?: number;
  name: string;
  type: string; // 'mindmap' or 'flowchart'
  data: any; // Store the diagram data as JSON
  thumbnail?: string; // Base64 encoded thumbnail image
  createdAt: Date;
  updatedAt: Date;
}

export interface InsertProject {
  userId?: number;
  name: string;
  type: string;
  data: any; // Must match Project interface
  thumbnail?: string;
}

export interface Template {
  id: number;
  name: string;
  type: string; // 'mindmap' or 'flowchart'
  data: any; // Store the template data as JSON
  thumbnail?: string; // Base64 encoded thumbnail image
  description?: string;
}

export interface InsertTemplate {
  name: string;
  type: string;
  data: any;
  thumbnail?: string;
  description?: string;
}

// Zod schemas for validation
export const insertUserSchema = z.object({
  username: z.string(),
  password: z.string()
});

// Make sure the schema matches the interface exactly
export const insertProjectSchema = z.object({
  userId: z.number().optional(),
  name: z.string(),
  type: z.string(),
  data: z.any().default({}), // Default empty object but still required
  thumbnail: z.string().optional()
});

export const insertTemplateSchema = z.object({
  name: z.string(),
  type: z.string(),
  data: z.any(),
  thumbnail: z.string().optional(),
  description: z.string().optional()
});
