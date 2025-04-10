import { Switch, Route } from "wouter";
import { Toaster } from "@/components/ui/toaster";
import Dashboard from "@/pages/Dashboard";
import MindMapPage from "@/pages/MindMapPage";
import FlowchartPage from "@/pages/FlowchartPage";
import AIGeneratorPage from "@/pages/AIGeneratorPage";
import NotFound from "@/pages/not-found";
import Navbar from "@/components/layout/Navbar";
import Sidebar from "@/components/layout/Sidebar";
import { useState, useEffect } from "react";
import { LoadingScreen } from "@/components/ui/loading-spinner";

function App() {
  const [projectName, setProjectName] = useState<string>("Untitled Project");
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Simulate loading time for app initialization
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2500); // 2.5 seconds loading time

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="bg-neutral-50 font-sans text-neutral-800 h-screen flex flex-col overflow-hidden">
      {isLoading ? (
        <LoadingScreen />
      ) : (
        <>
          <Navbar projectName={projectName} setProjectName={setProjectName} />
          
          <div className="flex-1 flex overflow-hidden">
            <Sidebar />
            
            <main className="flex-1 flex flex-col overflow-hidden">
              <Switch>
                <Route path="/" component={Dashboard} />
                <Route path="/mindmap/:id?">
                  {(params) => <MindMapPage id={params.id} setProjectName={setProjectName} />}
                </Route>
                <Route path="/flowchart/:id?">
                  {(params) => <FlowchartPage id={params.id} setProjectName={setProjectName} />}
                </Route>
                <Route path="/ai-generator" component={AIGeneratorPage} />
                <Route component={NotFound} />
              </Switch>
            </main>
          </div>
          
          <Toaster />
        </>
      )}
    </div>
  );
}

export default App;
