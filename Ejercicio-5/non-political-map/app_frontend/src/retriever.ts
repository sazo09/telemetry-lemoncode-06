import { fetchItems } from "./items.service";

export const setupRetriever = (element: HTMLButtonElement) => {
  element.addEventListener("click", async () => {
    console.log(window.location);

    try {
      const items = await fetchItems();
      console.log(items);
    } catch (error) {
      console.error(error);
    }
  });
};
