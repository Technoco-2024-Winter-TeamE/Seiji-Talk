import React, { useState } from "react";
import { Box, TextField, Button } from "@mui/material";
  
  

const LogoutButton: React.FC = () => {
    return (
      <Box display="flex" alignItems="center" justifyContent="flex-end" width="95%">
        <Button 
            variant="contained"
            sx={{
                minWidth: "130x",
                minHeight: "40px",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                color: "primary.light",
                backgroundColor: "primary.main",
            }}>
         Logout
        </Button>
      </Box>
    );
  };
  
  export default LogoutButton;