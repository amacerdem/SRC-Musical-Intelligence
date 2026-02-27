const { getDefaultConfig } = require("expo/metro-config");

// NativeWind temporarily disabled for web debugging
// const { withNativeWind } = require("nativewind/metro");
// module.exports = withNativeWind(config, { input: "./src/design/globals.css" });

module.exports = getDefaultConfig(__dirname);
