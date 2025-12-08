import React, { useEffect, useState } from 'react';
import { View, Text, Image, ActivityIndicator } from 'react-native';
import { styles } from '../../assets/my_styles';

export default function IndexScreen() {
  const [joke, setJoke] = useState(null);
  const [picture, setPicture] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('http://10.193.204.31:8000/api/random').then(res => res.json()),
      fetch('http://10.193.204.31:8000/api/random_picture').then(res => res.json())
    ]).then(([jokeData, picData]) => {
      setJoke(jokeData);
      setPicture(picData);
      setLoading(false);
    });
  }, []);

  if (loading) return <ActivityIndicator style={{ flex: 1 }} />;

  return (
    <View style={styles.container}>
      {picture && <Image source={{ uri: picture.image_url }} style={styles.image} />}
      {joke && <Text style={styles.jokeText}>{joke.text} - {joke.contributor}</Text>}
    </View>
  );
}
