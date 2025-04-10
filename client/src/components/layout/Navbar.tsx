import { useState } from "react";
import { Link, useLocation } from "wouter";
import { Moon, Sun, Pencil } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useToast } from "@/hooks/use-toast";

interface NavbarProps {
  projectName: string;
  setProjectName: (name: string) => void;
}

export default function Navbar({ projectName, setProjectName }: NavbarProps) {
  const [location, setLocation] = useLocation();
  const [tempName, setTempName] = useState(projectName);
  const [isEditingName, setIsEditingName] = useState(false);
  // Using only light theme - dark theme removed per request
  const { toast } = useToast();

  const isProjectPage =
    location.includes("/mindmap") || location.includes("/flowchart");

  const handleSaveName = () => {
    setProjectName(tempName);
    setIsEditingName(false);
  };

  const handleNewProject = () => {
    if (location.includes("/mindmap")) {
      setLocation("/mindmap");
    } else if (location.includes("/flowchart")) {
      setLocation("/flowchart");
    } else {
      setLocation("/");
    }
  };

  return (
    <header className="bg-white border-b border-neutral-200 shadow-sm z-10">
      <div className="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and Project Title */}
          <div className="flex-shrink-0 flex items-center">
            <div className="flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-8 w-8 text-primary-500"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path d="M5.5 13a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 13H9.366a.75.75 0 000 1.5h4.234A4.001 4.001 0 0012 9.749a5.5 5.5 0 00-6.5-5.244V4a3 3 0 00-3 3c0 1.657 1.343 3 3 3h7.5a3 3 0 10-1.396-5.663A5.5 5.5 0 005.5 13z" />
              </svg>
              <Link href="/">
                <span className="ml-2 text-xl font-bold text-primary-600 cursor-pointer">
                  FlowMind AI
                </span>
              </Link>
            </div>
          </div>

          {/* Project Controls */}
          {isProjectPage && (
            <div className="flex items-center">
              <div className="flex items-center ml-4">
                <span className="text-sm text-neutral-500 mr-2">
                  {projectName}
                </span>
                <button
                  onClick={() => setIsEditingName(true)}
                  className="text-neutral-400 hover:text-neutral-500"
                >
                  <Pencil size={16} />
                </button>
              </div>

              <div className="border-l border-neutral-200 h-6 mx-4"></div>

              <div className="flex space-x-4">
                <Button
                  variant="outline"
                  size="sm"
                  className="flex items-center"
                >
                  <span className="material-icons text-sm mr-1">save</span>
                  Save
                </Button>
              </div>
            </div>
          )}

          {/* User Menu */}
          <div className="flex items-center ml-6">
            {/* User Menu */}
            <div className="ml-3 relative">
              <div>
                <button className="flex items-center max-w-xs bg-white rounded-full focus:outline-none">
                  <span className="inline-block h-8 w-8 rounded-full overflow-hidden bg-neutral-200">
                    <svg
                      className="h-full w-full text-neutral-400"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Project Name Edit Dialog */}
      <Dialog open={isEditingName} onOpenChange={setIsEditingName}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Project Name</DialogTitle>
          </DialogHeader>
          <Input
            value={tempName}
            onChange={(e) => setTempName(e.target.value)}
            autoFocus
          />
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setIsEditingName(false)}>
              Cancel
            </Button>
            <Button onClick={handleSaveName}>Save</Button>
          </div>
        </DialogContent>
      </Dialog>
    </header>
  );
}
