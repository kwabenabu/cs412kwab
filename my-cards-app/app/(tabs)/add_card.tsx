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
  label: { fontSize: 14, fontWeight: '600', marginTop: 12, marginBottom: 6 },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
  },
  button: {
    marginTop: 20,
    backgroundColor: '#2563eb',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
});
