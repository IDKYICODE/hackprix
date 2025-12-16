import { View, Text, StyleSheet, ScrollView } from "react-native";
import { LinearGradient } from 'expo-linear-gradient';

export default function Home() {
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.headerTitle}>EduVerse</Text>
      <Text style={styles.headerSubtitle}>Your Immersive Learning Journey</Text>

      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Text style={styles.statText}>Streak</Text>
          <Text style={styles.statValue}>7</Text>
          <Text style={styles.statUnit}>days</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statText}>XP</Text>
          <Text style={styles.statValue}>2450</Text>
          <Text style={styles.statUnit}>points</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statText}>Coins</Text>
          <Text style={styles.statValue}>850</Text>
          <Text style={styles.statUnit}>tokens</Text>
        </View>
      </View>

      <View style={styles.dailyQuestContainer}>
        <View style={styles.dailyQuestHeader}>
          <Text style={styles.dailyQuestTitle}>Daily Quest</Text>
          <Text style={styles.dailyQuestXP}>+100 XP</Text>
        </View>
        <Text style={styles.dailyQuestDescription}>Watch 1 lesson + Play 1 VR Game</Text>
        <View style={styles.progressBarBackground}>
          <View style={styles.progressBarFill}></View>
        </View>
        <Text style={styles.dailyQuestProgressText}>1/2 completed</Text>
      </View>

      <Text style={styles.subjectsTitle}>Your Subjects</Text>
      <View style={styles.subjectsContainer}>
        <View style={styles.subjectCard}>
          <Text style={styles.subjectName}>Mathematics</Text>
          <View style={styles.subjectProgressBarBackground}>
            <View style={[styles.subjectProgressBarFill, {width: '65%'}]}></View>
          </View>
          <Text style={styles.subjectProgressText}>65% Complete</Text>
        </View>
        <View style={styles.subjectCard}>
          <Text style={styles.subjectName}>Physics</Text>
          <View style={styles.subjectProgressBarBackground}>
            <View style={[styles.subjectProgressBarFill, {width: '42%'}]}></View>
          </View>
          <Text style={styles.subjectProgressText}>42% Complete</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f0f2f5',
    padding: 20,
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#007bff',
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#6c757d',
    marginBottom: 20,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  statCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    alignItems: 'center',
    width: '32%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
    elevation: 3,
  },
  statText: {
    fontSize: 14,
    color: '#6c757d',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
  statUnit: {
    fontSize: 12,
    color: '#6c757d',
  },
  dailyQuestContainer: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
    elevation: 3,
  },
  dailyQuestHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  dailyQuestTitle: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  dailyQuestXP: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#28a745',
  },
  dailyQuestDescription: {
    fontSize: 14,
    color: '#6c757d',
    marginTop: 5,
  },
  progressBarBackground: {
    backgroundColor: '#e9ecef',
    height: 10,
    borderRadius: 5,
    marginTop: 10,
  },
  progressBarFill: {
    backgroundColor: '#007bff',
    height: 10,
    borderRadius: 5,
    width: '50%',
  },
  dailyQuestProgressText: {
    fontSize: 12,
    color: '#6c757d',
    marginTop: 5,
  },
  subjectsTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subjectsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  subjectCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 20,
    width: '48%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
    elevation: 3,
  },
  subjectName: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subjectProgressBarBackground: {
    backgroundColor: '#e9ecef',
    height: 8,
    borderRadius: 4,
    marginBottom: 5,
  },
  subjectProgressBarFill: {
    backgroundColor: '#007bff',
    height: 8,
    borderRadius: 4,
  },
  subjectProgressText: {
    fontSize: 12,
    color: '#6c757d',
  },
});
