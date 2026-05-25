const host = import.meta.env.VITE_BACKEND_URL ?? "";

export const fetchItems = async (): Promise<{ name: string }[] | null> => {
  const apiUrl = `${host}/api/items/`;

  try {
    console.log(`fetching from: ${apiUrl}`);
    const response = await fetch(apiUrl);

    console.log(response.url);

    if (response.ok) {
      return response.json();
    } else {
      const error = await response.text();
      console.error(error);
      return null;
    }
  } catch (error) {
    console.warn("network error");
    throw error;
  }
};
