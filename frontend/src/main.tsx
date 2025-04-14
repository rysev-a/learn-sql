import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import "./index.css";
import Layout from "./Layout.tsx";
import { BooksTable } from "./tables/BooksTable.tsx";
import { TagsTable } from "./tables/TagsTable.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<div>main page</div>} />
          <Route path="/books" element={<BooksTable />} />
          <Route path="/tags" element={<TagsTable />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
