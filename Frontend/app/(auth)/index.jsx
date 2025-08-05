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
import * as SecureStore from "expo-secure-store";
import { generateCodeVerifier, generateCodeChallenge } from "../../utils/pkce";

const Login = () => {
  const handleSubmit = async () => {
    try {
      const verifier = generateCodeVerifier();
      const challenge = await generateCodeChallenge(verifier);

      await SecureStore.setItemAsync("fitbit_verifier", verifier);

      const params = new URLSearchParams({
        client_id: "23QPTP",
        response_type: "code",
        scope: "activity heartrate sleep profile",
        redirect_uri:
          "https://310a8db79933.ngrok-free.app/fitbit/mobile-callback",
        code_challenge: challenge,
        code_challenge_method: "S256",
        state: "<optional_random_state>",
      });

      const authUrl = `https://www.fitbit.com/oauth2/authorize?${params.toString()}`;
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

      if (code) {
        const verifier = await SecureStore.getItemAsync("fitbit_verifier");

        const res = await fetch(
          " https://310a8db79933.ngrok-free.app/fitbit/token",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code, code_verifier: verifier }),
          }
        );

        const result = await res.json();
        console.log("✅ Logged in:", result);
        router.replace("/profile");
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
