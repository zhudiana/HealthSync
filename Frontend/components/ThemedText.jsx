import { Text, View, useColorScheme } from "react-native";
import React from "react";
import { Colors } from "../constants/Colors";

const ThemedText = ({ style, title = false, ...props }) => {
  const colorScheme = useColorScheme();
  const theme = Colors[colorScheme] ?? Colors.light;

  const textColor = title ? theme.title : theme.text;

  return <Text style={[{ color: textColor }, style]} {...props} />;
};

export default ThemedText;
