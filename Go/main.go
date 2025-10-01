package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"google.golang.org/api/option"
	"google.golang.org/api/sheets/v4"
)

func main() {

	fmt.Println("Hello, World!")
	start()
}

func start() {
	// Load credentials from the JSON file
	credentialsFile := "credentials.json"
	ctx := context.Background()
	srv, err := sheets.NewService(ctx, option.WithCredentialsFile(credentialsFile))
	if err != nil {
		log.Fatalf("Unable to retrieve Sheets client: %v", err)
	}

	// Define the spreadsheet ID and range
	spreadsheetID := "your-spreadsheet-id"
	readRange := "Sheet1!A1:D10"

	// Fetch the data
	resp, err := srv.Spreadsheets.Values.Get(spreadsheetID, readRange).Do()
	if err != nil {
		log.Fatalf("Unable to retrieve data from sheet: %v", err)
	}

	// Print the data
	if len(resp.Values) == 0 {
		fmt.Println("No data found.")
	} else {
		for _, row := range resp.Values {
			rowJSON, _ := json.Marshal(row)
			fmt.Println(string(rowJSON))
		}
	}
}
