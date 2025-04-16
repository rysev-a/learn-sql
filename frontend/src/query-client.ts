import axios, { AxiosError, AxiosResponse } from "axios";
import { toast } from "sonner";
import { QueryClient, useQuery, useMutation } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false, // default: true
      staleTime: 1000 * 60 * 60,
    },
  },
});

export interface BaseModelType {
  id: string;
}

export interface BookType extends BaseModelType {
  name: string;
  description: string;
}

export interface UserType extends BaseModelType {
  email: string;
  first_name: string;
  last_name: string;
}

export interface TagType {
  id: string;
  name: string;
  description: string;
}

export const crudApi = <ModelType extends BaseModelType>(url: string) => ({
  getList: (
    pagination: { limit: number; offset: number } = { limit: 100, offset: 0 },
  ) =>
    axios.get(`${url}?limit=${pagination.limit}&offset=${pagination.offset}`),
  removeDetail: (id: string) => axios.delete(`${url}/${id}`), //.then((res: { data: ModelType }) => res.data),
  updateDetail: (data: Partial<ModelType>) =>
    axios.patch(`${url}/${data.id}`, data),
  createDetail: (data: Partial<ModelType>) =>
    axios.post(url, data).then((res: { data: ModelType }) => res.data),
});

export const onSuccessRemove =
  <ModelType extends BaseModelType>(queryKey: string) =>
  (_data: AxiosResponse, id: string) => {
    queryClient.setQueryData([queryKey], (items: ModelType[]) => {
      return items.filter((item) => item.id !== id);
    });
  };

export const onSuccessUpdate =
  <ModelType extends BaseModelType>(queryKey: string) =>
  ({ data }: { data: ModelType }) => {
    queryClient.setQueryData([queryKey], (items: ModelType[]) => {
      return items.map((item) => (item.id === data.id ? data : item));
    });
  };

export const onSuccessCreate =
  <ModelType extends BaseModelType>(queryKey: string) =>
  (item: ModelType) => {
    queryClient.setQueryData([queryKey], (items: ModelType[]) => {
      return [...items, item];
    });
  };

export interface Pagination {
  limit: number;
  offset: number;
}

export const useConfigureQuery = <ModelType extends BaseModelType>(
  queryKey: string,
  url: string,
  pagination?: Pagination,
) => {
  const api = crudApi<ModelType>(url);

  const list = useQuery({
    queryKey: [queryKey, pagination],
    queryFn: async () => {
      try {
        const response = await api.getList(pagination);
        return response.data;
      } catch (e) {
        return Promise.reject(new Error((e as AxiosError).message));
      }
    },
  });

  if (list.error) {
    toast.error(`Can't load ${queryKey} - ${list.error}`);
  }

  return {
    list,
    remove: useMutation({
      mutationFn: api.removeDetail,
      onSuccess: onSuccessRemove<ModelType>(queryKey),
      onError: () => {
        toast.error("Failed to remove");
      },
    }),
    update: useMutation({
      mutationFn: api.updateDetail,
      onSuccess: onSuccessUpdate<ModelType>(queryKey),
    }),
    create: useMutation({
      mutationFn: api.createDetail,
      onSuccess: onSuccessCreate<ModelType>(queryKey),
    }),
  };
};

export const useApiQuery = () => {
  // const books = useConfigureQuery<BookType>("books", "/api/books/books");
  // const tags = useConfigureQuery<TagType>("tags", "/api/books/tags");
  const users = useConfigureQuery<UserType>("users", "/api/users");
  return { users };
};
