import type { NextConfig } from "next";

const isProd = process.env.NODE_ENV === 'production';
const repo = 'Portfolio';

const nextConfig: NextConfig = {
  output: 'export',
  basePath: isProd ? `/${repo}` : '', 
  assetPrefix: isProd ? `/${repo}` : '', 
  images: { unoptimized: isProd },
};

export default nextConfig;
