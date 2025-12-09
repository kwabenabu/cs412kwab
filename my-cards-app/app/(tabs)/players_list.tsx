import React from 'react';
import { View, Text, FlatList, Image, StyleSheet } from 'react-native';
import { mockPlayers } from '../../src/mockData';

export default function PlayersListScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Players</Text>
      <FlatList
        data={mockPlayers}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.player}>
            <Image source={{ uri: item.image }} style={styles.image} />
            <View style={styles.info}>
              <Text style={styles.name}>{item.full_name}</Text>
              <Text>{item.position} - {item.club_team}</Text>
              <Text>{item.country}</Text>
            </View>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 16 },
  player: { flexDirection: 'row', marginBottom: 16, backgroundColor: '#f9f9f9', borderRadius: 8, overflow: 'hidden', elevation: 2 },
  image: { width: 80, height: 80, resizeMode: 'cover', borderRadius: 40 },
  placeholder: { width: 80, height: 80, backgroundColor: '#ddd', borderRadius: 40 },
  info: { flex: 1, padding: 12, justifyContent: 'center' },
  name: { fontWeight: 'bold', fontSize: 16 },
});
