/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // ensure Next.js can proxy api requests to localhost:8000
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8000/:path*',
      },
    ]
  },
}

module.exports = nextConfig
