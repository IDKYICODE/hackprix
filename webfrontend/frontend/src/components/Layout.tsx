import { ReactNode } from "react";
import BottomNav from "./BottomNav";
import AIChatbot from "./AIChatbot";

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen bg-background">
      {children}
      <AIChatbot />
      <BottomNav />
    </div>
  );
};

export default Layout;