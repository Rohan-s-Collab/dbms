export interface DummyUser {
  id: string;
  name: string;
  email: string;
  role: "exporter" | "provider";
  companyName: string;
}
