import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import "./index.css";
import Layout from "./Layout.tsx";
// import { BooksTable } from "./tables/BooksTable.tsx";
// import { TagsTable } from "./tables/TagsTable.tsx";
import UserListPage from "@/pages/users/UserListPage";
import RoleListPage from "@/pages/roles/RoleListPage";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<div>main page</div>} />
          <Route path="/users" element={<UserListPage />} />
          <Route path="/roles" element={<RoleListPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
