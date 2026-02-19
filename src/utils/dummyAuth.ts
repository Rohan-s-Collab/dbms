import type { DummyUser } from "../types/user";


const DUMMY_USER_KEY = "dummyUser";

// 🔹 Create dummy user
export const createDummyUser = (user: DummyUser) => {
  localStorage.setItem(DUMMY_USER_KEY, JSON.stringify(user));
};

// 🔹 Get dummy user
export const getDummyUser = (): DummyUser | null => {
  const data = localStorage.getItem(DUMMY_USER_KEY);
  return data ? JSON.parse(data) : null;
};

// 🔹 Remove dummy user
export const logoutDummyUser = () => {
  localStorage.removeItem(DUMMY_USER_KEY);
};
