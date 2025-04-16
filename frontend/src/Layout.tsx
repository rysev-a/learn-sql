import { Toaster } from "@/components/ui/sonner";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./query-client";
import { Link, Outlet } from "react-router";

const Layout = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="p-10 min-h-svh">
        <Link to="/" className="mr-5">start</Link>
        <Link to="/users" className="mr-5">users</Link>
        <Link to="/roles">roles</Link>
        <Outlet />
        <Toaster />
      </div>
    </QueryClientProvider>
  );
};

export default Layout;
