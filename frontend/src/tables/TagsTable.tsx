import { toast } from "sonner";

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
import { TagType, useApiQuery } from "@/query-client";
import { useNavigate } from "react-router";

export interface Role {
  id: string;
  name: string;
}

export function TagsTable() {
  const form = useForm();
  const { tags } = useApiQuery();
  const navigate = useNavigate();

  const onSubmit = (data: Partial<TagType>) => {
    if (data.id) {
      tags.update.mutateAsync(data).then(() => {
        toast("update success");
      });
    }

    // else {
    //   tags.create
    //     .mutateAsync(data)
    //     .then(() => {
    //       toast.success("create success");
    //       navigate("/");
    //     })
    //     .catch(() => {
    //       toast.error("can't create ");
    //     });
    // }
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
          {tags.list.isSuccess
            ? tags.list.data.map((book) => (
                <TableRow key={book.id}>
                  <TableCell className="font-medium">
                    {book.id} {book.a}
                  </TableCell>
                  <TableCell>{book.name}</TableCell>
                  <TableCell>
                    {book.description}{" "}
                    <Button
                      variant={"outline"}
                      className="cursor-pointer"
                      onClick={() => tags.remove.mutate(book.id)}
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
