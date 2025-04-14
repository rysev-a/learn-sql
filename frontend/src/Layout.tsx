import { Toaster } from "@/components/ui/sonner";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./query-client";
import { Link, Outlet } from "react-router";

const Layout = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="p-10 min-h-svh">
        <Link to="/books" className="mr-5">
          books
        </Link>
        <Link to="/tags">tags</Link>
        <Outlet />
        <Toaster />
      </div>
    </QueryClientProvider>
  );
};

export default Layout;
