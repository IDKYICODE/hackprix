import { View, Text, TextInput, TouchableOpacity, ActivityIndicator, ScrollView, Platform } from "react-native";
import { useState } from "react";
import { useRouter } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { useAuth } from "../../context/AuthContext";

export default function SignupScreen() {
  const router = useRouter();
  const { register } = useAuth();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form Data State
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    password2: "", // Added confirm password field
    role: "student", // default
    gender: "",
    date_of_birth: "",
    institution: "",
    mobile_number: "",
    bio: ""
  });

  const updateFormData = (key: string, value: string) => {
    setFormData(prev => ({ ...prev, [key]: value }));
  };

  const validateStep1 = () => {
    if (!formData.username || !formData.email || !formData.password || !formData.password2) {
      setError("Please fill in all fields.");
      return false;
    }
    if (formData.password !== formData.password2) {
      setError("Passwords do not match.");
      return false;
    }
    setError(null);
    return true;
  };

  const validateStep2 = () => {
    if (!formData.role || !formData.gender || !formData.date_of_birth) {
      setError("Please fill in all personal details.");
      return false;
    }
    // Basic date regex check YYYY-MM-DD
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(formData.date_of_birth)) {
      setError("Date of Birth must be in YYYY-MM-DD format.");
      return false;
    }
    setError(null);
    return true;
  };

  const handleNext = () => {
    if (step === 1 && validateStep1()) {
      setStep(2);
    } else if (step === 2 && validateStep2()) {
      setStep(3);
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
      setError(null);
    } else {
      router.back();
    }
  };

  const handleSignup = async () => {
    setLoading(true);
    setError(null);

    try {
      // Call register from context which handles API and state update
      await register(formData);

      // No need to manually navigate if auth state change handles it in _layout,
      // but to be safe we can redirect if needed.
      // The _layout.tsx usually watches 'user' state and redirects to tabs.
    } catch (err: any) {
      console.error("Registration error:", err);
      // Display a more meaningful error if possible
      const msg = err.response?.data?.detail || err.message || "Registration failed. Please try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignup = () => {
      // Logic for Google Signup (likely populates step 1 and moves to step 2)
      console.log("Google Signup");
      // For demo purposes, let's prefill and move next
      setFormData(prev => ({...prev, username: "GoogleUser", email: "google@example.com", password: "google_token_placeholder", password2: "google_token_placeholder" }));
      setStep(2);
  };

  // --- Render Steps ---

  const renderStep1 = () => (
    <>
      <Text style={{ fontSize: 24, fontWeight: "700", marginBottom: 8, color: '#333' }}>
        Create Account
      </Text>
      <Text style={{ color: "#666", marginBottom: 24 }}>
        Step 1: Account Information
      </Text>

      {/* Google Sign Up Button */}
      <TouchableOpacity
        onPress={handleGoogleSignup}
        style={{
          backgroundColor: "#fff",
          padding: 14,
          borderRadius: 12,
          alignItems: "center",
          flexDirection: 'row',
          justifyContent: 'center',
          borderWidth: 1,
          borderColor: '#ccc',
          marginBottom: 24
        }}
      >
        <Ionicons name="logo-google" size={20} color="#DB4437" style={{ marginRight: 8 }} />
        <Text style={{ color: "#333", fontWeight: "600" }}>
          Sign up with Google
        </Text>
      </TouchableOpacity>

      <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 24 }}>
        <View style={{ flex: 1, height: 1, backgroundColor: '#eee' }} />
        <Text style={{ marginHorizontal: 8, color: '#999' }}>OR</Text>
        <View style={{ flex: 1, height: 1, backgroundColor: '#eee' }} />
      </View>

      <TextInput
        placeholder="Username"
        value={formData.username}
        onChangeText={(text) => updateFormData("username", text)}
        autoCapitalize="none"
        style={styles.input}
      />
      <TextInput
        placeholder="Email"
        value={formData.email}
        onChangeText={(text) => updateFormData("email", text)}
        autoCapitalize="none"
        keyboardType="email-address"
        style={styles.input}
      />
      <TextInput
        placeholder="Password"
        secureTextEntry
        value={formData.password}
        onChangeText={(text) => updateFormData("password", text)}
        style={styles.input}
      />

      {/* Added Confirm Password Field */}
      <TextInput
        placeholder="Confirm Password"
        secureTextEntry
        value={formData.password2}
        onChangeText={(text) => updateFormData("password2", text)}
        style={styles.input}
      />
    </>
  );

  const renderStep2 = () => (
    <>
      <Text style={{ fontSize: 24, fontWeight: "700", marginBottom: 8, color: '#333' }}>
        Personal Details
      </Text>
      <Text style={{ color: "#666", marginBottom: 24 }}>
        Step 2: Tell us about yourself
      </Text>

      <Text style={styles.label}>I am a:</Text>
      <View style={{ flexDirection: 'row', marginBottom: 16 }}>
          {['student', 'teacher'].map((role) => (
              <TouchableOpacity
                  key={role}
                  onPress={() => updateFormData("role", role)}
                  style={[
                      styles.optionButton,
                      formData.role === role && styles.optionButtonSelected
                  ]}
              >
                  <Text style={[
                      styles.optionText,
                      formData.role === role && styles.optionTextSelected
                  ]}>
                      {role.charAt(0).toUpperCase() + role.slice(1)}
                  </Text>
              </TouchableOpacity>
          ))}
      </View>

      <Text style={styles.label}>Gender:</Text>
      <View style={{ flexDirection: 'row', marginBottom: 16 }}>
          {['male', 'female', 'other'].map((gender) => (
              <TouchableOpacity
                  key={gender}
                  onPress={() => updateFormData("gender", gender)}
                  style={[
                      styles.optionButton,
                      formData.gender === gender && styles.optionButtonSelected,
                      { marginRight: 8 }
                  ]}
              >
                  <Text style={[
                      styles.optionText,
                      formData.gender === gender && styles.optionTextSelected
                  ]}>
                      {gender.charAt(0).toUpperCase() + gender.slice(1)}
                  </Text>
              </TouchableOpacity>
          ))}
      </View>

      <Text style={styles.label}>Date of Birth (YYYY-MM-DD):</Text>
      <TextInput
        placeholder="YYYY-MM-DD"
        value={formData.date_of_birth}
        onChangeText={(text) => updateFormData("date_of_birth", text)}
        style={styles.input}
        keyboardType="numeric"
      />
    </>
  );

  const renderStep3 = () => (
    <>
      <Text style={{ fontSize: 24, fontWeight: "700", marginBottom: 8, color: '#333' }}>
        Final Details
      </Text>
      <Text style={{ color: "#666", marginBottom: 24 }}>
        Step 3: Almost there!
      </Text>

      <TextInput
        placeholder="Institution Name"
        value={formData.institution}
        onChangeText={(text) => updateFormData("institution", text)}
        style={styles.input}
      />

      <TextInput
        placeholder="Mobile Number"
        value={formData.mobile_number}
        onChangeText={(text) => updateFormData("mobile_number", text)}
        keyboardType="phone-pad"
        style={styles.input}
      />

      <TextInput
        placeholder="Bio (Optional)"
        value={formData.bio}
        onChangeText={(text) => updateFormData("bio", text)}
        multiline
        numberOfLines={3}
        style={[styles.input, { height: 80, textAlignVertical: 'top' }]}
      />
    </>
  );

  return (
    <ScrollView contentContainerStyle={{ flexGrow: 1, justifyContent: "center", padding: 24, backgroundColor: '#fff' }}>

      {/* Progress Bar */}
      <View style={{ flexDirection: 'row', height: 4, backgroundColor: '#eee', marginBottom: 32, borderRadius: 2 }}>
          <View style={{ flex: step / 3, backgroundColor: '#00E5FF', borderRadius: 2 }} />
      </View>

      {error && (
        <Text style={{ color: "red", marginBottom: 16 }}>{error}</Text>
      )}

      {step === 1 && renderStep1()}
      {step === 2 && renderStep2()}
      {step === 3 && renderStep3()}

      <View style={{ flexDirection: 'row', marginTop: 16 }}>
          {step > 1 && (
            <TouchableOpacity
                onPress={handleBack}
                disabled={loading}
                style={[styles.button, { backgroundColor: '#f0f0f0', marginRight: 12 }]}
            >
                <Text style={{ color: "#333", fontWeight: "600" }}>Back</Text>
            </TouchableOpacity>
          )}

          <TouchableOpacity
            onPress={step === 3 ? handleSignup : handleNext}
            disabled={loading}
            style={[styles.button, { backgroundColor: loading ? "#aaa" : "#00E5FF", flex: 1 }]}
          >
            {loading ? (
                <ActivityIndicator size="small" color="#fff" />
            ) : (
                <Text style={{ color: "#fff", fontWeight: "600" }}>
                    {step === 3 ? "Complete Registration" : "Next"}
                </Text>
            )}
          </TouchableOpacity>
      </View>

      {step === 1 && (
        <TouchableOpacity onPress={() => router.back()} style={{ marginTop: 24, alignItems: 'center' }}>
            <Text style={{ color: "#00E5FF", fontWeight: "600" }}>
            Already have an account? Login
            </Text>
        </TouchableOpacity>
      )}
    </ScrollView>
  );
}

const styles = {
    input: {
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 12,
        padding: 14,
        marginBottom: 16,
        fontSize: 16,
    },
    button: {
        padding: 16,
        borderRadius: 14,
        alignItems: "center" as const,
        justifyContent: "center" as const,
    },
    label: {
        fontSize: 14,
        fontWeight: "600" as const,
        marginBottom: 8,
        color: '#333'
    },
    optionButton: {
        paddingVertical: 10,
        paddingHorizontal: 16,
        borderRadius: 20,
        borderWidth: 1,
        borderColor: '#ddd',
        marginRight: 10,
        backgroundColor: '#f9f9f9',
    },
    optionButtonSelected: {
        backgroundColor: '#e0faff',
        borderColor: '#00E5FF',
    },
    optionText: {
        color: '#666',
    },
    optionTextSelected: {
        color: '#007a8a',
        fontWeight: "600" as const,
    }
};
