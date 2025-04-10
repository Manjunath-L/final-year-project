import { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useToast } from '@/hooks/use-toast';
import MindMapEditorNew from '@/components/editor/MindMapEditorNew';
import { apiRequest } from '@/lib/queryClient';
import { queryClient } from '@/lib/queryClient';
import html2canvas from 'html2canvas';

interface MindMapPageProps {
  id?: string;
  setProjectName: (name: string) => void;
}

interface MindMapData {
  rootId: string;
  nodes: Record<string, any>;
}

interface Project {
  id: number;
  name: string;
  type: 'mindmap' | 'flowchart';
  data: MindMapData;
  thumbnail?: string;
  createdAt: Date;
  updatedAt: Date;
}

export default function MindMapPage({ id, setProjectName }: MindMapPageProps) {
  const { toast } = useToast();
  const [mindMapData, setMindMapData] = useState<MindMapData | undefined>(undefined);
  
  // Fetch project data if id is provided
  const { data: project, isLoading } = useQuery<Project>({
    queryKey: id ? [`/api/projects/${id}`] : ['/api/dummy-key'],
    enabled: !!id,
  });
  
  // Set project data and name when loaded
  useEffect(() => {
    if (project) {
      setProjectName(project.name);
      setMindMapData(project.data);
    } else if (!id) {
      // New project
      setProjectName('Untitled Mind Map');
      setMindMapData({
        rootId: '1',
        nodes: {
          '1': { id: '1', text: 'Central Idea', children: [] }
        }
      });
    }
  }, [project, id, setProjectName]);
  
  // Mutation for saving the project
  const saveMutation = useMutation({
    mutationFn: async (data: MindMapData) => {
      // Simple thumbnail generation
      const element = document.querySelector('.mindmap-canvas');
      let thumbnail = '';
      
      if (element) {
        try {
          const canvas = await html2canvas(element as HTMLElement);
          thumbnail = canvas.toDataURL('image/png');
        } catch (error) {
          console.error('Error generating thumbnail:', error);
        }
      }
      
      if (id) {
        // Update existing project
        return apiRequest('PUT', `/api/projects/${id}`, {
          data,
          thumbnail,
          updatedAt: new Date()
        });
      } else {
        // Create new project
        return apiRequest('POST', '/api/projects', {
          name: 'Untitled Mind Map',
          type: 'mindmap',
          data,
          thumbnail,
          userId: 1 // Default user ID for demo
        });
      }
    },
    onSuccess: () => {
      toast({
        title: 'Success',
        description: 'Mind map saved successfully',
      });
      
      queryClient.invalidateQueries({ queryKey: ['/api/projects'] });
    },
    onError: () => {
      toast({
        title: 'Error',
        description: 'Failed to save mind map',
        variant: 'destructive',
      });
    }
  });
  
  // Handle save
  const handleSave = (data: MindMapData) => {
    saveMutation.mutate(data);
  };
  
  if (isLoading && id) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-700 mx-auto"></div>
          <p className="mt-2 text-neutral-600">Loading mind map...</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="flex-1 flex flex-col mindmap-canvas">
      {mindMapData && (
        <MindMapEditorNew
          initialData={mindMapData}
          onSave={handleSave}
        />
      )}
    </div>
  );
}
