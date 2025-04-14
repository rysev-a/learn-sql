import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useForm } from "react-hook-form";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useApiQuery } from "@/query-client";
import { useEffect } from "react";

export interface Role {
  id: string;
  name: string;
}

export interface Book {
  id: string;
  name: string;
  description: string;
}

export function BooksTable() {
  const { books } = useApiQuery();

  const form = useForm();
  const onSubmit = (data: Partial<Book>) => {
    if (data.id) {
      books.update.mutateAsync(data).then(() => {
        console.log("Navigate to main page");
      });
    }

    const postData = { description: data.description };
    books.create.mutateAsync(postData).then(() => {
      console.log("Navigate to main page");
    });
  };

  return (
    <div>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <div className="w-100 py-10">
          <Label htmlFor="name">Name</Label>
          <Input
            type="name"
            id="name"
            placeholder="Name"
            {...form.register("name")}
          />
        </div>

        <div className="w-100 py-10">
          <Label htmlFor="description">Description</Label>
          <Input
            type="description"
            id="description"
            placeholder="Description"
            {...form.register("description")}
          />
        </div>
        <Button>Save</Button>
      </form>

      <Table>
        <TableCaption>A list of your recent invoices.</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>id</TableHead>
            <TableHead>name</TableHead>
            <TableHead className="text-right">description</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          {books.list.isSuccess
            ? books.list.data.map((book) => (
                <TableRow key={book.id}>
                  <TableCell className="font-medium">{book.id}</TableCell>
                  <TableCell>{book.name}</TableCell>
                  <TableCell>
                    {book.description}{" "}
                    <Button
                      variant={"outline"}
                      className="cursor-pointer"
                      onClick={() => books.remove.mutate(book.id)}
                    >
                      remove
                    </Button>
                    <Button
                      variant={"outline"}
                      className="cursor-pointer"
                      onClick={() => {
                        form.setValue("id", book.id);
                        form.setValue("name", book.name);
                        form.setValue("description", book.description);
                      }}
                    >
                      set
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            : null}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell colSpan={3}>Total</TableCell>
          </TableRow>
        </TableFooter>
      </Table>
    </div>
  );
}
