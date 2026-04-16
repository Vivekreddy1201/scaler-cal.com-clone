"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Calendar, Clock, Link as LinkIcon } from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Event types", href: "/", icon: LinkIcon },
  { name: "Bookings", href: "/bookings", icon: Calendar },
  { name: "Availability", href: "/availability", icon: Clock },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <>
      <div className="hidden md:flex h-full w-56 flex-col border-r border-gray-200 bg-gray-50 px-4 py-6 dark:border-zinc-800 dark:bg-gradient-to-b dark:from-[#222222] dark:to-[#111111]">
        <div className="mb-8 flex items-center px-2">
          <div className="flex h-8 w-8 items-center justify-center rounded bg-gray-900 text-white font-bold dark:bg-white dark:text-black">
            C
          </div>
          <span className="ml-3 text-lg font-bold text-gray-900 dark:text-white">Cal Clone</span>
        </div>
        
        <nav className="flex-1 space-y-1">
          {navigation.map((item) => {
            const isActive = pathname === item.href || (item.href === "/" && pathname.startsWith("/events")) || (item.href !== "/" && pathname.startsWith(item.href));
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "group flex items-center rounded-xl px-3.5 py-2.5 text-[15px] font-medium transition-colors mb-1.5",
                  isActive
                    ? "bg-zinc-200 text-zinc-900 dark:bg-zinc-800 dark:text-white"
                    : "text-zinc-600 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-900/40 dark:hover:text-white"
                )}
              >
                <item.icon
                  className={cn(
                    "mr-3.5 h-[1.125rem] w-[1.125rem] flex-shrink-0 stroke-[2]",
                    isActive ? "text-zinc-900 dark:text-white" : "text-zinc-500 dark:text-zinc-400 dark:group-hover:text-zinc-300"
                  )}
                  aria-hidden="true"
                />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Mobile Bottom Tab Navigation */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 flex justify-between border-t border-gray-200 bg-white px-6 py-3 dark:border-zinc-800 dark:bg-[#111]">
        {navigation.map((item) => {
          const isActive = pathname === item.href || (item.href === "/" && pathname.startsWith("/events")) || (item.href !== "/" && pathname.startsWith(item.href));
          return (
            <Link
              key={item.name}
              href={item.href}
              className="flex flex-col items-center justify-center gap-1"
            >
              <item.icon
                className={cn(
                  "h-6 w-6 stroke-[2]",
                  isActive ? "text-zinc-900 dark:text-white" : "text-zinc-500 dark:text-zinc-400"
                )}
                aria-hidden="true"
              />
              <span className={cn("text-[10px] font-medium", isActive ? "text-zinc-900 dark:text-white" : "text-zinc-500 dark:text-zinc-400")}>
                {item.name}
              </span>
            </Link>
          );
        })}
      </div>
    </>
  );
}
