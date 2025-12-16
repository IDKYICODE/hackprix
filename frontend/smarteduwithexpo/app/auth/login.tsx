import { View, Text, TextInput, TouchableOpacity, ActivityIndicator } from "react-native";
import { useState } from "react";
import { useAuth } from "../../context/AuthContext";

export default function LoginScreen() {
  // The useAuth hook is now the single source of truth for the login action.
  const { login } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async () => {
    if (!username || !password) {
      setError("Username and password are required");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // We only need to call the login function from the context.
      // It will handle the API request, token storage, and state updates.
      await login(username, password);
      // On success, the root layout will automatically navigate to the main app.
    } catch (err) {
      // The context now re-throws the error, so we can catch it here.
      setError("Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: "center", padding: 24, backgroundColor: '#fff' }}>
      <Text style={{ fontSize: 32, fontWeight: "700", marginBottom: 8, color: '#333' }}>
        EduVerse
      </Text>

      <Text style={{ color: "#666", marginBottom: 32 }}>
        Your Immersive Learning Journey
      </Text>

      {error && (
        <Text style={{ color: "red", marginBottom: 12 }}>{error}</Text>
      )}

      <TextInput
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
        style={{
          borderWidth: 1,
          borderColor: '#ccc',
          borderRadius: 12,
          padding: 14,
          marginBottom: 16,
        }}
      />

      <TextInput
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
        style={{
          borderWidth: 1,
          borderColor: '#ccc',
          borderRadius: 12,
          padding: 14,
          marginBottom: 24,
        }}
      />

      <TouchableOpacity
        onPress={handleLogin}
        disabled={loading}
        style={{
          backgroundColor: loading ? "#aaa" : "#00E5FF",
          padding: 16,
          borderRadius: 14,
          alignItems: "center",
          flexDirection: 'row',
          justifyContent: 'center'
        }}
      >
        {loading && <ActivityIndicator size="small" color="#fff" style={{marginRight: 8}}/>}
        <Text style={{ color: "#fff", fontWeight: "600" }}>
          {loading ? "Logging in..." : "Login"}
        </Text>
      </TouchableOpacity>
    </View>
  );
}
