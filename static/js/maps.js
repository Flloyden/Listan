function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
      mapTypeControl: false,
      center: { lat: 55.6088, lng: 12.9946 },
      zoom: 11,
    });

    new AutocompleteDirectionsHandler(map);
  }
  
  class AutocompleteDirectionsHandler {
    map;
    originPlaceId;
    destinationPlaceId;
    travelMode;
    directionsService;
    directionsRenderer;

    
    constructor(map) {
      this.map = map;
      this.originPlaceId = "";
      this.destinationPlaceId = "";
      this.travelMode = google.maps.TravelMode.WALKING;
      this.directionsService = new google.maps.DirectionsService();
      this.directionsRenderer = new google.maps.DirectionsRenderer();
      this.directionsRenderer.setMap(map);
  
      const originInput = document.getElementById("origin-input");
      const destinationInput = document.getElementById("destination-input");
      const modeSelector = document.getElementById("mode-selector");
      const originAutocomplete = new google.maps.places.Autocomplete(originInput);
  
      // Specify just the place data fields that you need.
      originAutocomplete.setFields(["place_id"]);
  
      const destinationAutocomplete = new google.maps.places.Autocomplete(
        destinationInput
      );
  
      // Specify just the place data fields that you need.
      destinationAutocomplete.setFields(["place_id"]);
      this.setupClickListener(
        "WALKING",
        google.maps.TravelMode.WALKING
      );
      this.setupClickListener(
        "BICYCLING",
        google.maps.TravelMode.BICYCLING
      );
      this.setupClickListener(
        "TRANSIT",
        google.maps.TravelMode.TRANSIT
      );
      this.setupClickListener(
        "DRIVING",
        google.maps.TravelMode.DRIVING
      );
      this.setupPlaceChangedListener(originAutocomplete, "ORIG");
      this.setupPlaceChangedListener(destinationAutocomplete, "DEST");
      this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(originInput);
      this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(
        destinationInput
      );
      this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(modeSelector);
    }
    // Sets a listener on a radio button to change the filter type on Places
    // Autocomplete.
    setupClickListener(id, mode) {
      const radioButton = document.getElementById(id);
  
      radioButton.addEventListener("click", () => {
        this.travelMode = mode;
        this.route();
      });
    }
    setupPlaceChangedListener(autocomplete, mode) {
      autocomplete.bindTo("bounds", this.map);
      autocomplete.addListener("place_changed", () => {
        const place = autocomplete.getPlace();
  
        if (!place.place_id) {
          window.alert("Var god välj en plats från listan.");
          return;
        }
  
        if (mode === "ORIG") {
          this.originPlaceId = place.place_id;
        } else {
          this.destinationPlaceId = place.place_id;
        }
  
        this.route();
      });
    }
    route() {
      if (!this.originPlaceId || !this.destinationPlaceId) {
        return;
      }
  
      const me = this;
  
      this.directionsService.route(
        {
          origin: { placeId: this.originPlaceId },
          destination: { placeId: this.destinationPlaceId },
          travelMode: this.travelMode,
        },
        (response, status) => {
          if (status === "OK") {
            me.directionsRenderer.setDirections(response);

            var originInput = document.getElementById('origin-input').value;
            var destinationInput = document.getElementById('destination-input').value;

            var service = new google.maps.DistanceMatrixService();
            service.getDistanceMatrix(
              {
                origins: [originInput],
                destinations: [destinationInput],
                travelMode: this.travelMode,
              }, callback);

              function callback(response, status) {
                if(status === "OK") {
                  console.log(response);

                    var results = response.rows[0].elements;
                      var element = results[0];
                      var duration = element.duration.text;
                      var duration_seconds = element.duration.value;
                      var from = response.originAddresses;
                      var to = response.destinationAddresses;
                      document.getElementById("number").setAttribute('value',duration_seconds);
                      document.getElementById("city").setAttribute('value',from + " " + to);
                      document.getElementById("headertag").innerHTML = duration;
                } else {
                  window.alert("Not great at all");
                }
              }

          } else {
            window.alert("Directions request failed due to " + status);
          }
        }
      );
    }
  }