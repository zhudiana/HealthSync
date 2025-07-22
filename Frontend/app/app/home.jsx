import { StyleSheet, Text, View, Image } from "react-native";
import React from "react";
import { Button } from "@react-navigation/elements";
import { Link } from "expo-router";
import ThemedView from "../../components/ThemedView";
import ThemedLogo from "../../components/ThemedLogo";
import Spacer from "../../components/Spacer";
import ThemedText from "../../components/ThemedText";

const Home = () => {
  return (
    <>
      <Link href={"/profile"} style={styles.link}>
        <ThemedText>HOme page</ThemedText>;
      </Link>
      <Link href={"/dashboard"} style={styles.link}>
        <ThemedText>HOme page</ThemedText>;
      </Link>
      <Link href={"/devices"} style={styles.link}>
        <ThemedText>HOme page</ThemedText>;
      </Link>
      <Link href={"/notification"} style={styles.link}>
        <ThemedText>HOme page</ThemedText>;
      </Link>
    </>
  );
};

export default Home;

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
  buttonContainer: {},
});
