import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import * as ImagePicker from "expo-image-picker";
import { Ionicons } from "@expo/vector-icons";
import { useState, useEffect } from "react";

import { useAuth } from "@/context/AuthContext";
import { updateProfile } from "@/lib/authClient";

import { Platform } from "react-native";

const BACKEND_BASE_URL =
  Platform.OS === "android"
    ? "http://10.0.2.2:8000"
    : "http://192.168.31.114:8000";


export default function Profile() {
  const { user, loading, setUser } = useAuth();

  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);

  const [bio, setBio] = useState("");
  const [mobile, setMobile] = useState("");

  /* -----------------------------
     Sync local state when user loads
  -------------------------------- */
  useEffect(() => {
    if (user) {
      setBio(user.bio ?? "");
      setMobile(user.mobile_number ?? "");
    }
  }, [user]);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#2575fc" />
      </View>
    );
  }

  if (!user) {
    return (
      <View style={styles.center}>
        <Text>Not logged in</Text>
      </View>
    );
  }

  /* -----------------------------
     Image Picker (NEW API)
  -------------------------------- */
 const pickImage = async () => {
   const result = await ImagePicker.launchImageLibraryAsync({
     mediaTypes: ["images"],
     allowsEditing: true,
     aspect: [1, 1],
     quality: 0.7,
   });

   if (!result.canceled) {
     const img = result.assets[0];
     const formData = new FormData();

     formData.append("profile_image", {
       uri: img.uri,
       name: "profile.jpg",
       type: "image/jpeg",
     } as any);

     const updated = await updateProfile(formData);
     setUser(updated);
   }
 };

  /* -----------------------------
     Save Profile
  -------------------------------- */
  const saveProfile = async () => {
    try {
      setSaving(true);

      const formData = new FormData();
      formData.append("bio", bio);
      formData.append("mobile_number", mobile);

      const updated = await updateProfile(formData);
      setUser(updated);
      setEditing(false);
    } finally {
      setSaving(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <View style={styles.headerRow}>
        <Text style={styles.headerTitle}>Profile</Text>

        <TouchableOpacity
          onPress={() => setEditing((prev) => !prev)}
          hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
          style={styles.editButton}
          activeOpacity={0.6}
        >
          <Ionicons
            name={editing ? "close" : "pencil"}
            size={22}
            color="#007bff"
          />
        </TouchableOpacity>
      </View>

      <Text style={styles.headerSubtitle}>
        Identity, edited with intent
      </Text>

      {/* Profile Card */}
      <LinearGradient
        colors={["#6a11cb", "#2575fc"]}
        style={styles.profileCard}
      >
        <TouchableOpacity onPress={pickImage} activeOpacity={0.8}>
          <Image
            source={{
              uri: user.profile_image
                ? `${BACKEND_BASE_URL}${user.profile_image}`
                : "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",

            }}
            style={styles.profileImage}
          />
        </TouchableOpacity>

        <Text style={styles.profileName}>{user.username}</Text>

        <Text style={styles.profileMeta}>
          {user.role.toUpperCase()}
        </Text>

        <Text style={styles.profileMeta}>
          {user.institution_name ?? "Independent Learner"}
        </Text>
      </LinearGradient>

      {/* Editable Fields */}
      <View style={styles.section}>
        <Text style={styles.label}>Bio</Text>
        {editing ? (
          <TextInput
            value={bio}
            onChangeText={setBio}
            placeholder="Write something about yourself"
            style={styles.input}
            multiline
          />
        ) : (
          <Text style={styles.valueText}>
            {bio || "No bio yet"}
          </Text>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.label}>Mobile</Text>
        {editing ? (
          <TextInput
            value={mobile}
            onChangeText={setMobile}
            keyboardType="phone-pad"
            style={styles.input}
          />
        ) : (
          <Text style={styles.valueText}>
            {mobile || "Not added"}
          </Text>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.label}>Email</Text>
        <Text style={styles.valueText}>{user.email}</Text>
      </View>

      {/* Save Button */}
      {editing && (
        <TouchableOpacity
          style={styles.saveButton}
          onPress={saveProfile}
          disabled={saving}
        >
          <Text style={styles.saveText}>
            {saving ? "Saving..." : "Save Changes"}
          </Text>
        </TouchableOpacity>
      )}
    </ScrollView>
  );
}

/* =============================
   Styles
============================= */
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f0f2f5",
    padding: 20,
  },

  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },

  headerRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  editButton: {
    padding: 6,
  },

  headerTitle: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#007bff",
  },

  headerSubtitle: {
    fontSize: 16,
    color: "#6c757d",
    marginBottom: 20,
  },

  profileCard: {
    borderRadius: 15,
    padding: 20,
    alignItems: "center",
    marginBottom: 20,
  },

  profileImage: {
    width: 90,
    height: 90,
    borderRadius: 45,
    borderWidth: 3,
    borderColor: "#fff",
    marginBottom: 10,
  },

  profileName: {
    color: "#fff",
    fontSize: 22,
    fontWeight: "bold",
  },

  profileMeta: {
    color: "#e0e0ff",
    fontSize: 14,
    marginTop: 4,
  },

  section: {
    marginBottom: 15,
  },

  label: {
    fontSize: 14,
    color: "#6c757d",
    marginBottom: 5,
  },

  valueText: {
    fontSize: 16,
    color: "#212529",
    backgroundColor: "#fff",
    padding: 12,
    borderRadius: 8,
  },

  input: {
    backgroundColor: "#fff",
    padding: 12,
    borderRadius: 8,
    fontSize: 16,
  },

  saveButton: {
    backgroundColor: "#007bff",
    padding: 15,
    borderRadius: 10,
    alignItems: "center",
    marginTop: 10,
  },

  saveText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
  },
});
