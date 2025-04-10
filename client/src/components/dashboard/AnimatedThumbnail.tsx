import React from "react";
import { z } from "zod";

// Define strict types for thumbnail component
const DiagramTypeSchema = z.enum(['mindmap', 'flowchart']);
type DiagramType = z.infer<typeof DiagramTypeSchema>;

interface AnimatedThumbnailProps {
  type: DiagramType;
  name: string;
  size?: 'sm' | 'md' | 'lg';
}

export default function AnimatedThumbnail({ type, name, size = 'md' }: AnimatedThumbnailProps) {
  // Adjust sizes based on the size prop
  const containerClasses = {
    sm: "w-16 h-16",
    md: "w-24 h-24",
    lg: "w-32 h-32"
  };

  if (type === 'mindmap') {
    return (
      <div className={`thumbnail-animated ${containerClasses[size]} rounded-lg bg-neutral-50`}>
        <div className="thumbnail-mindmap-preview">
          {/* Central node */}
          <div className="thumbnail-mindmap-node root"></div>
          
          {/* Branch nodes - positioned with absolute positioning */}
          <div className="thumbnail-mindmap-node branch" style={{ top: '30%', left: '30%' }}></div>
          <div className="thumbnail-mindmap-node branch" style={{ top: '30%', right: '30%' }}></div>
          <div className="thumbnail-mindmap-node branch" style={{ bottom: '30%', left: '30%' }}></div>
          <div className="thumbnail-mindmap-node branch" style={{ bottom: '30%', right: '30%' }}></div>
          
          {/* Leaf nodes with different animations */}
          <div className="thumbnail-mindmap-node leaf" style={{ top: '20%', left: '20%' }}></div>
          <div className="thumbnail-mindmap-node leaf" style={{ top: '20%', right: '20%' }}></div>
          <div className="thumbnail-mindmap-node leaf" style={{ bottom: '20%', left: '20%' }}></div>
          <div className="thumbnail-mindmap-node leaf" style={{ bottom: '20%', right: '20%' }}></div>
        </div>
      </div>
    );
  }
  
  return (
    <div className={`thumbnail-animated ${containerClasses[size]} rounded-lg bg-neutral-50`}>
      <div className="thumbnail-flowchart-preview">
        {/* Top terminal node */}
        <div className="thumbnail-flowchart-node terminal thumbnail-fade"></div>
        
        {/* Process nodes */}
        <div className="thumbnail-flowchart-node process thumbnail-slide"></div>
        
        {/* Decision node */}
        <div className="thumbnail-flowchart-node decision"></div>
        
        {/* More process nodes */}
        <div className="thumbnail-flowchart-node process thumbnail-slide" style={{ animationDelay: "0.5s" }}></div>
        
        {/* Bottom terminal node */}
        <div className="thumbnail-flowchart-node terminal thumbnail-fade" style={{ animationDelay: "0.3s" }}></div>
      </div>
    </div>
  );
}