import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to Soccer Cards</Text>
      <Text style={styles.subtitle}>Browse cards, view details, and meet the players.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 8 },
  subtitle: { fontSize: 16, color: '#555', textAlign: 'center' },
});
