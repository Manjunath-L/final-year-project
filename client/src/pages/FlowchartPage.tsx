import { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useToast } from '@/hooks/use-toast';
import FlowchartEditor from '@/components/editor/FlowchartEditor';
import { Node, Edge } from 'reactflow';
import { apiRequest } from '@/lib/queryClient';
import { queryClient } from '@/lib/queryClient';
import html2canvas from 'html2canvas';

interface FlowchartPageProps {
  id?: string;
  setProjectName: (name: string) => void;
}

interface FlowchartData {
  nodes: Node[];
  edges: Edge[];
}

interface Project {
  name: string;
  data: FlowchartData;
}

export default function FlowchartPage({ id, setProjectName }: FlowchartPageProps) {
  const { toast } = useToast();
  const [flowchartData, setFlowchartData] = useState<FlowchartData | undefined>(undefined);
  
  // Fetch project data if id is provided
  const { data: project, isLoading } = useQuery<Project>({
    queryKey: id ? [`/api/projects/${id}`] : [],
    enabled: !!id,
  });
  
  // Set project data and name when loaded
  useEffect(() => {
    if (project) {
      setProjectName(project.name);
      setFlowchartData(project.data);
    } else if (!id) {
      // New project
      setProjectName('Untitled Flowchart');
      setFlowchartData({
        nodes: [
          { id: '1', type: 'input', data: { label: 'Start' }, position: { x: 250, y: 0 } },
          { id: '2', data: { label: 'Process Step' }, position: { x: 250, y: 100 } },
          { id: '3', type: 'output', data: { label: 'End' }, position: { x: 250, y: 200 } }
        ],
        edges: [
          { id: 'e1-2', source: '1', target: '2', animated: false },
          { id: 'e2-3', source: '2', target: '3', animated: false }
        ]
      });
    }
  }, [project, id, setProjectName]);
  
  // Mutation for saving the project
  const saveMutation = useMutation({
    mutationFn: async (data: FlowchartData) => {
      // Generate a thumbnail from the flowchart
      const element = document.querySelector('.react-flow');
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
          name: 'Untitled Flowchart',
          type: 'flowchart',
          data,
          thumbnail,
          userId: 1 // Default user ID for demo
        });
      }
    },
    onSuccess: () => {
      toast({
        title: 'Success',
        description: 'Flowchart saved successfully',
      });
      
      // Invalidate projects query
      queryClient.invalidateQueries({ queryKey: ['/api/projects'] });
    },
    onError: () => {
      toast({
        title: 'Error',
        description: 'Failed to save flowchart',
        variant: 'destructive',
      });
    }
  });
  
  // Handle save
  const handleSave = (nodes: Node[], edges: Edge[]) => {
    saveMutation.mutate({ nodes, edges });
  };
  
  if (isLoading && id) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-700 mx-auto"></div>
          <p className="mt-2 text-neutral-600">Loading flowchart...</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="flex-1 flex flex-col">
      {flowchartData && (
        <FlowchartEditor
          initialNodes={flowchartData.nodes}
          initialEdges={flowchartData.edges}
          onSave={handleSave}
        />
      )}
    </div>
  );
}
