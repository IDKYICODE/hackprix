import { Stack, useRouter, useSegments } from "expo-router";
import { AuthProvider, useAuth } from "../context/AuthContext";
import { ActivityIndicator, View } from "react-native";
import { useEffect } from "react";

const InitialLayout = () => {
  // Now we check for the user object instead of a boolean
  const { user, loading } = useAuth();
  const router = useRouter();
  const segments = useSegments();

  useEffect(() => {
    console.log("[Layout] Auth state changed. Loading:", loading, "User:", user);
    if (loading) return; // Wait until the auth state is fully loaded

    const inTabsGroup = segments[0] === "tabs";

    // If the user is not signed in and they are not in the auth section,
    // redirect them to the login screen.
    if (!user && !inTabsGroup) {
      console.log("[Layout] User not found and not in auth group, redirecting to login.");
      router.replace("/auth/login");
    }
    // If the user is signed in and they are in the auth section,
    // redirect them to the main app screen.
    else if (user && inTabsGroup === false) {
      console.log("[Layout] User found and not in tabs group, redirecting to home.");
      router.replace("/tabs/Home");
    }
  }, [user, loading, segments, router]);

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="tabs" options={{ headerShown: false }} />
      <Stack.Screen name="auth/login" options={{ headerShown: false }} />
    </Stack>
  );
};

export default function RootLayout() {
  return (
    <AuthProvider>
      <InitialLayout />
    </AuthProvider>
  );
}
