import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';
import { mockPlayers } from '../../src/mockData';

export default function ProfileScreen() {
  const me = mockPlayers[0];

  return (
    <View style={styles.container}>
      <Image source={{ uri: me.image }} style={styles.avatar} />
      <Text style={styles.name}>{me.full_name}</Text>
      <Text style={styles.meta}>{me.position} · {me.club_team}</Text>
      <Text style={styles.meta}>{me.country}</Text>
      <View style={styles.statsRow}>
        <View style={styles.stat}>
          <Text style={styles.statValue}>15</Text>
          <Text style={styles.statLabel}>Cards Owned</Text>
        </View>
        <View style={styles.stat}>
          <Text style={styles.statValue}>5</Text>
          <Text style={styles.statLabel}>Sets Completed</Text>
        </View>
        <View style={styles.stat}>
          <Text style={styles.statValue}>$7.2k</Text>
          <Text style={styles.statLabel}>Portfolio</Text>
        </View>
      </View>
      <Text style={styles.sectionTitle}>About</Text>
      <Text style={styles.about}>
        Collector since 2020. Favorite players: Mbappé, Haaland, and Putellas. Always chasing the rarest inserts.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 20, alignItems: 'center' },
  avatar: { width: 120, height: 120, borderRadius: 60, marginBottom: 12 },
  name: { fontSize: 22, fontWeight: 'bold' },
  meta: { fontSize: 14, color: '#555' },
  statsRow: { flexDirection: 'row', marginTop: 20, width: '100%', justifyContent: 'space-between' },
  stat: { flex: 1, alignItems: 'center' },
  statValue: { fontSize: 18, fontWeight: 'bold' },
  statLabel: { fontSize: 12, color: '#666' },
  sectionTitle: { alignSelf: 'flex-start', marginTop: 24, fontSize: 16, fontWeight: 'bold' },
  about: { marginTop: 8, fontSize: 14, color: '#444', lineHeight: 20 },
});
