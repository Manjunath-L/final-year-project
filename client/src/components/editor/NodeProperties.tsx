import { useState, useEffect } from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';

interface NodeProps {
  id: string;
  text: string;
  children?: string[] | null;
  color?: string;
  shape?: string;
  fontSize?: string;
  fontFamily?: string;
}

interface NodePropertiesProps {
  node: NodeProps;
  onUpdateProperty: (property: string, value: any) => void;
  onDelete?: (nodeId: string) => void;
}

// Color palette
const colors = [
  { name: 'White', value: '#ffffff' },
  { name: 'Green', value: '#4CAF50' },
  { name: 'Red', value: '#f44336' },
  { name: 'Blue', value: '#2196F3' },
  { name: 'Yellow', value: '#FFC107' },
  { name: 'Purple', value: '#9C27B0' },
  { name: 'Cyan', value: '#00BCD4' },
  { name: 'Pink', value: '#E91E63' },
  { name: 'Orange', value: '#FF9800' },
  { name: 'Light Blue', value: '#03A9F4' },
  { name: 'Lime', value: '#CDDC39' },
  { name: 'Teal', value: '#009688' },
];


export default function NodeProperties({ node, onUpdateProperty, onDelete }: NodePropertiesProps) {
  const [text, setText] = useState(node.text);
  const [isExpanded, setIsExpanded] = useState(true);
  
  // Update the text state when the selected node changes
  useEffect(() => {
    setText(node.text);
  }, [node.id, node.text]);
  
  // Handle text change and update after a short delay
  const handleTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setText(e.target.value);
  };
  
  // Update the node property when text input loses focus
  const handleTextBlur = () => {
    onUpdateProperty('text', text);
  };
  
  // Update color
  const handleColorChange = (color: string) => {
    onUpdateProperty('color', color);
  };
  
  // Update font
  const handleFontChange = (font: string) => {
    onUpdateProperty('fontFamily', font);
  };
  
  // Update font size
  const handleFontSizeChange = (size: string) => {
    onUpdateProperty('fontSize', size);
  };
  
  // Toggle properties panel expansion
  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };
  
  // Handle node deletion
  const handleDelete = () => {
    if (onDelete) {
      onDelete(node.id);
    }
  };
  
  return (
    <div 
      className="border-l border-neutral-200 bg-white overflow-hidden transition-all duration-300 ease-in-out flex flex-col"
      style={{ 
        width: isExpanded ? 'clamp(250px, 20vw, 300px)' : '40px',
        minWidth: isExpanded ? '200px' : '40px',
      }}
    >
      {/* Header with toggle button */}
      <div className="flex items-center justify-between p-3 border-b border-neutral-200 sticky top-0 bg-white z-10">
        {isExpanded ? (
          <h3 className="font-medium text-neutral-800">Properties</h3>
        ) : (
          <span className="material-icons text-neutral-600 mx-auto rotate-90">tune</span>
        )}
        
        <button
          onClick={toggleExpand}
          className="flex-shrink-0 text-neutral-500 hover:text-neutral-700 focus:outline-none"
        >
          <span className="material-icons text-lg">
            {isExpanded ? 'chevron_right' : 'chevron_left'}
          </span>
        </button>
      </div>
      
      {isExpanded && (
        <div className="p-4 overflow-y-auto flex-1">
          <Tabs defaultValue="general">
            <TabsList className="w-full mb-4">
              <TabsTrigger value="general" className="flex-1">General</TabsTrigger>
              <TabsTrigger value="style" className="flex-1">Style</TabsTrigger>
            </TabsList>
            
            <TabsContent value="general" className="space-y-4">
              <div>
                <Label className="block text-sm font-medium text-neutral-700 mb-1">Text</Label>
                <Input
                  type="text"
                  value={text}
                  onChange={handleTextChange}
                  onBlur={handleTextBlur}
                  className="w-full"
                />
              </div>

              {onDelete && (
                <div className="pt-4 border-t border-neutral-200">
                  <Button
                    variant="destructive"
                    className="w-full"
                    onClick={handleDelete}
                  >
                    Delete Node
                  </Button>
                </div>
              )}
            </TabsContent>
            
            <TabsContent value="style" className="space-y-4">
              <div>
                <Label className="block text-sm font-medium text-neutral-700 mb-1">Fill Color</Label>
                <div className="grid grid-cols-6 gap-2 mt-1">
                  {colors.map((color) => (
                    <button 
                      key={color.value}
                      className="w-6 h-6 rounded-full relative"
                      style={{ backgroundColor: color.value }}
                      title={color.name}
                      onClick={() => handleColorChange(color.value)}
                    >
                      {node.color === color.value && (
                        <span className="absolute inset-0 flex items-center justify-center">
                          <span className="material-icons text-sm text-neutral-800">check</span>
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              </div>
              
              <div>
                <Label className="block text-sm font-medium text-neutral-700 mb-1">Font Family</Label>
                <Select 
                  value={node.fontFamily || 'sans'} 
                  onValueChange={handleFontChange}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select font family" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="sans">Sans Serif</SelectItem>
                    <SelectItem value="serif">Serif</SelectItem>
                    <SelectItem value="mono">Monospace</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label className="block text-sm font-medium text-neutral-700 mb-1">Font Size</Label>
                <Select 
                  value={node.fontSize || 'md'} 
                  onValueChange={handleFontSizeChange}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select font size" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="sm">Small</SelectItem>
                    <SelectItem value="md">Medium</SelectItem>
                    <SelectItem value="lg">Large</SelectItem>
                    <SelectItem value="xl">Extra Large</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      )}
    </div>
  );
}
