import { Sidebar } from "./Sidebar";

export function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen w-full flex-col md:flex-row overflow-hidden bg-white dark:bg-[#111]">
      <Sidebar />
      <main className="flex-1 overflow-y-auto bg-white md:bg-gray-50/50 pb-16 md:pb-0 dark:bg-[#111]">
        <div className="w-full h-full p-4 md:p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
