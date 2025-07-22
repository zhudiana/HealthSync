import { StyleSheet, Text, View, Image, Pressable } from "react-native";
import React from "react";
import { Button } from "@react-navigation/elements";
import { Link, Stack } from "expo-router";
import ThemedView from "../../components/ThemedView";
import ThemedLogo from "../../components/ThemedLogo";
import Spacer from "../../components/Spacer";
import ThemedText from "../../components/ThemedText";
import { Colors } from "../../constants/Colors";
import ThemedButton from "../../components/ThemedButton";

const Login = () => {
  const handleSubmit = () => {
    console.log("logged in with fitbit");
  };
  return (
    <ThemedView style={styles.container}>
      {/* <ThemedLogo /> */}

      <ThemedText style={styles.welcome} title={true}>
        Welcome to HealthSync
      </ThemedText>

      <ThemedText style={styles.title}>
        Connect your smart watch account to continue
      </ThemedText>

      <Spacer height={10} />

      <View style={styles.buttonContainer}>
        <ThemedButton onPress={handleSubmit}>
          <Text>Login with Fitbit</Text>
        </ThemedButton>
        <ThemedButton onPress={handleSubmit}>
          <Text>Login with Withings</Text>
        </ThemedButton>
      </View>

      <Link href={"/profile"} style={styles.link}>
        <ThemedText>profile page</ThemedText>;
      </Link>
    </ThemedView>
  );
};

export default Login;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  welcome: {
    fontWeight: "bold",
    fontSize: 30,
  },
  title: {
    fontWeight: "300",
    marginTop: 15,
    fontSize: 15,
  },
});
