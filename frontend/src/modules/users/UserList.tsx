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

import { ChevronDown } from "lucide-react";

import { Button } from "@/components/ui/button";

import { useConfigureQuery, UserType } from "@/query-client";
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  PaginationState,
} from "@tanstack/react-table";
import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { DataTablePagination } from "@/components/TablePagination";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
  DropdownMenuCheckboxItem,
} from "@/components/ui/dropdown-menu";
import { format, parseISO } from "date-fns";

const columns = [
  { header: "ID", accessorFn: (row: UserType) => row.id.slice(0, 4) },
  {
    header: "Email",
    accessorKey: "email",
  },
  {
    header: "first name",
    accessorKey: "first_name",
  },
  {
    header: "last_name",
    accessorFn: (row: UserType) => row.last_name,
  },
  {
    header: "birthdate",
    accessorFn: (row: UserType) => row.birthdate,
  },
];

export function UserList() {
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 10,
  });

  const [filterBirthdate, setFilterBirthdate] = useState(new Date());

  const formattedBirthDate = filterBirthdate
    ? format(filterBirthdate, "yyyy-MM-dd")
    : "";

  const users = useConfigureQuery<UserType>(
    "users",
    "/api/users",
    {
      offset: pagination.pageIndex * pagination.pageSize,
      limit: pagination.pageSize,
    },
    [
      {
        key: "birthdate",
        value: formattedBirthDate,
      },
    ],
  );

  const [data, setData] = useState<UserType[]>([]);

  useEffect(() => {
    if (users.list.isSuccess) {
      setData(users.list.data);
    }
  }, [users.list.isSuccess, users.list.data]);

  //...
  const table = useReactTable({
    columns,
    data,
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    rowCount: 500,
    manualPagination: true,
    state: {
      pagination,
    },
  });

  return (
    <div>
      <div className="flex items-center py-4">
        <Input
          placeholder="Filter emails..."
          type="date"
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            if (event?.currentTarget?.value) {
              setFilterBirthdate(parseISO(event?.currentTarget?.value));
            }
          }}
          className="max-w-sm"
        />
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-auto">
              Columns <ChevronDown />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {table
              .getAllColumns()
              .filter((column) => column.getCanHide())
              .map((column) => {
                return (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className="capitalize"
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) =>
                      column.toggleVisibility(!!value)
                    }
                  >
                    {column.id}
                  </DropdownMenuCheckboxItem>
                );
              })}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <Table>
        <TableCaption>A list of your recent invoices.</TableCaption>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return (
                  <TableHead key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext(),
                        )}
                  </TableHead>
                );
              })}
            </TableRow>
          ))}
        </TableHeader>

        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                data-state={row.getIsSelected() && "selected"}
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center">
                No results.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell colSpan={columns.length}>
              <DataTablePagination table={table} />
            </TableCell>
          </TableRow>
        </TableFooter>
      </Table>

      <div className="flex items-center justify-end space-x-2 py-4"></div>
    </div>
  );
}
