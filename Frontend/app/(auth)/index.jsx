import {
  StyleSheet,
  Text,
  View,
  Image,
  Pressable,
  Linking,
} from "react-native";
import React, { useEffect } from "react";
import { Button } from "@react-navigation/elements";
import { Link, Stack } from "expo-router";
import ThemedView from "../../components/ThemedView";
import ThemedLogo from "../../components/ThemedLogo";
import Spacer from "../../components/Spacer";
import ThemedText from "../../components/ThemedText";
import { Colors } from "../../constants/Colors";
import ThemedButton from "../../components/ThemedButton";

const Login = () => {
  const handleSubmit = async () => {
    try {
      const res = await fetch("http://192.168.137.32:8000/fitbit/login");
      const data = await res.json();
      const authUrl = data.url;
      const state = data.state;

      await Linking.openURL(authUrl);
    } catch (error) {
      console.log("Fitbit login failed: ", error);
    }
  };

  useEffect(() => {
    const handleDeepLink = async (event) => {
      const url = event.url;
      const parsed = new URL(url);
      const code = parsed.searchParams.get("code");
      const state = parsed.searchParams.get("state");

      if (code && state) {
        // Send code & state to FastAPI to get tokens
        const res = await fetch("http://192.168.137.32:8000/fitbit/callback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code, state }),
        });

        if (res.ok) {
          const result = await res.json();
          console.log("✅ Logged in:", result);
          router.replace("/profile"); // Move to dashboard
        } else {
          console.error("❌ Failed to exchange code");
        }
      }
    };

    const subscription = Linking.addEventListener("url", handleDeepLink);
    Linking.getInitialURL().then((url) => {
      if (url) handleDeepLink({ url });
    });

    return () => subscription.remove();
  }, []);
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
