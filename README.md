# Thing Finder PoC

This project is a Flask-based web application that allows users to log the location of their items and later find them by querying the system. The application manages user sessions to facilitate logging items, confirming item locations, and updating timestamps.

## Features

- **Log Item Locations**: Users can log the locations of their items along with a timestamp.
- **Find Item Locations**: Users can query the system to find the last known location and timestamp of their items.
- **Confirm Item Locations**: The application prompts users to confirm if the item is still at the logged location, allowing for updates if necessary.
- **Session Management**: The application uses sessions to manage ongoing interactions, such as logging new items or confirming existing item locations.
- **Data Persistence**: Item data is stored in a `data.json` file, ensuring data persistence across server restarts.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/thing-finder-poc.git
    cd thing-finder-poc
    ```

2. **Create and activate a virtual environment:**
    ```sh 
    conda create --name [thing-finder-poc] python=3.8
    conda activate thing-finder-poc
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```sh
    python app.py
    ```

5. **Open your browser and go to:**
    ```
    http://127.0.0.1:5000/
    ```

## Usage

1. **Log an Item Location:**
    - Input format: `log <item> at <location>`
    - Example: `log keys at kitchen`

2. **Find an Item Location:**
    - Input format: `find <item>` or `where is my <item>`
    - Example: `find keys` or `where is my keys`

3. **Confirm Item Location:**
    - When prompted with `Is the item still there? (yes/no)`, respond with `yes` or `no`.

## API Endpoints

- **`GET /`**: Renders the main page.
- **`POST /interact`**: Interacts with the user based on the input provided. The user input should be sent in the request body with the key `user_input`.

## Data Storage

- The item data is stored in a `data.json` file in the following format:
    ```json
    {
        "item_name": {
            "location": "location_name",
            "timestamp": "timestamp"
        },
        ...
    }
    ```

## Future To-dos

- Differtent users can log in and log their items maybe using mobile numbers as UID.
- Add a feature to delete the item from the list.
- Integration of database for better data management. maybe mongodb.
- Integrate with whatsapp bot. So that user can interact with the system using whatsapp. No need of anyweb interface. just type in whatsapp and get the location of the item. hassel free.

---
*Made with ❤️ Anish*