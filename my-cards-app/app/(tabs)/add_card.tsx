import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, Pressable, Alert, ScrollView } from 'react-native';
import { mockPlayers } from '../../src/mockData';

export default function AddCardScreen() {
  const [form, setForm] = useState({
    player: mockPlayers[1]?.full_name ?? 'Kylian Mbappé',
    set: 'Champions 2024',
    rarity: 'Epic',
    number: 'KM-07',
    value: '900',
  });

  const handlePress = () => {
    Alert.alert('Demo only', 'This is a presentation stub. No card was saved.');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Add a New Card</Text>
      <Text style={styles.helper}>Fields are prefilled with demo data—feel free to tweak them for the presentation.</Text>

      <Label text="Player" />
      <TextInput
        style={styles.input}
        value={form.player}
        onChangeText={(player) => setForm((f) => ({ ...f, player }))}
        placeholder="Player name"
      />

      <Label text="Set" />
      <TextInput
        style={styles.input}
        value={form.set}
        onChangeText={(set) => setForm((f) => ({ ...f, set }))}
        placeholder="Set name"
      />

      <Label text="Card Number" />
      <TextInput
        style={styles.input}
        value={form.number}
        onChangeText={(number) => setForm((f) => ({ ...f, number }))}
        placeholder="e.g., KM-07"
      />

      <Label text="Rarity" />
      <TextInput
        style={styles.input}
        value={form.rarity}
        onChangeText={(rarity) => setForm((f) => ({ ...f, rarity }))}
        placeholder="Common / Rare / Epic / Legendary"
      />

      <Label text="Estimated Value (USD)" />
      <TextInput
        style={styles.input}
        keyboardType="numeric"
        value={form.value}
        onChangeText={(value) => setForm((f) => ({ ...f, value }))}
        placeholder="Estimated value"
      />

      <Pressable style={styles.button} onPress={handlePress}>
        <Text style={styles.buttonText}>Save Card (Demo)</Text>
      </Pressable>
    </ScrollView>
  );
}

function Label({ text }: { text: string }) {
  return <Text style={styles.label}>{text}</Text>;
}

const styles = StyleSheet.create({
  container: { padding: 20, backgroundColor: '#fff' },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 8 },
  helper: { fontSize: 14, color: '#555', marginBottom: 16 },
  label: { fontSize: 14, fontWeight: 'bold', marginTop: 12, marginBottom: 6 },
  input: {
    borderWidth: 1,
  const [selectedPlayer, setSelectedPlayer] = useState<number | null>(null);
  const [cardNumber, setCardNumber] = useState('');
  const [rarity, setRarity] = useState('');
  const [estimatedValue, setEstimatedValue] = useState('');
  const [players, setPlayers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const API_URL = 'https://cs-webapps.bu.edu/kwabamp/project/api/players/';

  React.useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        setPlayers(data.results || data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

// Styles should be outside the component
const styles = StyleSheet.create({
  container: { padding: 20, backgroundColor: '#fff' },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 8 },
  helper: { fontSize: 14, color: '#555', marginBottom: 16 },
  label: { fontSize: 14, fontWeight: '600', marginTop: 12, marginBottom: 6 },
  input: {
    borderWidth: 1,
    fontSize: 16,
    marginBottom: 8,
  },
  button: {
    marginTop: 20,
    backgroundColor: '#2563eb',
    paddingVertical: 12,
  },
});
