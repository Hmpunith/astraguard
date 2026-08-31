/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  webpack: (config, { webpack, isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        path: false,
        url: false,
      };
    }
    // Define Cesium base URL
    config.plugins.push(
      new webpack.DefinePlugin({
        CESIUM_BASE_URL: JSON.stringify('/cesium'),
      })
    );
    return config;
  },
  // Copy Cesium static files
  async rewrites() {
    return [];
  },
  transpilePackages: ['cesium'],
};

export default nextConfig;
