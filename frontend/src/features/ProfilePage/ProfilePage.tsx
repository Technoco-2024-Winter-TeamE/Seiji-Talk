import React, { useState } from "react";
import { Box, TextField, Button, Typography } from "@mui/material";

const ProfilePage: React.FC = () => {
  const [birthDate, setBirthDate] = useState<string>("");
  const [residence, setResidence] = useState<string>("");
  const [registry, setRegistry] = useState<string>("");

  const handleSave = () => {
    console.log("保存:", { birthDate, residence, registry });
  };

  return (
    <Box style={{ padding: "20px" }}>
      <Typography variant="h4" gutterBottom>
        プロフィール設定
      </Typography>
      <TextField
        label="生年月日"
        type="date"
        InputLabelProps={{ shrink: true }}
        fullWidth
        value={birthDate}
        onChange={(e) => setBirthDate(e.target.value)}
        style={{ marginBottom: "10px" }}
      />
      <TextField
        label="居住地"
        fullWidth
        value={residence}
        onChange={(e) => setResidence(e.target.value)}
        style={{ marginBottom: "10px" }}
      />
      <TextField
        label="住民票所在地"
        fullWidth
        value={registry}
        onChange={(e) => setRegistry(e.target.value)}
        style={{ marginBottom: "10px" }}
      />
      <Button variant="contained" color="primary" onClick={handleSave}>
        保存
      </Button>
    </Box>
  );
};

export default ProfilePage;
