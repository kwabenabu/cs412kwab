import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Image, ActivityIndicator } from 'react-native';
import { styles } from '../../assets/my_styles';

const API_URL = 'http://10.193.204.31:8000/project/api/players/';

export default function PlayersListScreen() {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        setPlayers(data.results || data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return <ActivityIndicator size="large" style={{ flex: 1 }} />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Players</Text>
      <FlatList
        data={players}
        keyExtractor={(item) => item.id?.toString() || item.pk?.toString()}
        renderItem={({ item }) => (
          <View style={styles.player}>
            {item.image ? (
              <Image source={{ uri: item.image }} style={styles.image} />
            ) : (
              <View style={styles.placeholder} />
            )}
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
