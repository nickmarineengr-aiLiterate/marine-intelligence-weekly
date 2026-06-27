import { NextResponse } from "next/server";

const PROTECTED_PATH = "/meoclass1";
const PASSWORD = process.env.QB_ACCESS_PASSWORD || "meo2026";
const COOKIE_NAME = "miw_qb_access";
const COOKIE_MAX_AGE = 60 * 60 * 24 * 30; // 30 days

export function middleware(request) {
  const { pathname } = request.nextUrl;

  // Only protect /meoclass1 paths
  if (!pathname.startsWith(PROTECTED_PATH)) {
    return NextResponse.next();
  }

  // Allow access to login page itself
  if (pathname === "/meoclass1/login") {
    return NextResponse.next();
  }

  // Check cookie
  const cookie = request.cookies.get(COOKIE_NAME);
  if (cookie && cookie.value === PASSWORD) {
    return NextResponse.next();
  }

  // Redirect to login
  const loginUrl = new URL("/meoclass1/login", request.url);
  loginUrl.searchParams.set("redirect", pathname);
  return NextResponse.redirect(loginUrl);
}

export const config = {
  matcher: ["/meoclass1/:path*"],
};
