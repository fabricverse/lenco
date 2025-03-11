// Copyright (c) 2025, Adam Dawoodjee and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payment Link", {
	refresh(frm) {
        set_vendor_name(frm);
        set_route(frm)
	},
    vendor_name(frm){
        // set_vendor_name(frm);
    },
    route(frm){
        // set_route(frm);
    },
    validate(frm){
        set_vendor_name(frm);
        set_route(frm);
    }
});

function set_vendor_name(frm){
    if(frm.doc.vendor_name) return;
    frm.set_value("vendor_name", frappe.session.user_fullname);
    refresh_field('vendor_name');
}

function set_route(frm) {
    if (frm.doc.route) return;
  
    const userPart = frappe.session.user_fullname.toLowerCase().replace(/ /g, "-");
  
    const randomWords = generateRandomWords(3); // Generate 3 random words
    const docPart = randomWords.join("-"); // Join words with dashes
  
    generated_route = `${userPart}-${docPart}`;
    frm.set_value("route", generated_route);
    refresh_field("route");
  }
  
  function generateRandomWords(count) {
    /**
     * Generates an array of random words.
     */
    const words = [
      "apple", "banana", "cherry", "date", "elderberry", "fig", "grape",
      "honeydew", "kiwi", "lemon", "mango", "nectarine", "orange", "papaya",
      "quince", "raspberry", "strawberry", "tangerine", "watermelon", "zebra",
      "sun", "moon", "star", "cloud", "rain", "wind", "fire", "water", "earth",
      "sky", "tree", "flower", "bird", "fish", "house", "book", "pen", "car",
      "city", "river", "mountain", "forest", "ocean", "island", "desert",
      "valley", "peak", "summit", "road", "path", "bridge", "tunnel", "gate",
      "wall", "tower", "castle", "palace", "garden", "park", "field", "meadow",
      "lake", "pond", "stream", "spring", "well", "cave", "rock", "stone",
      "sand", "soil", "grass", "leaf", "branch", "root", "fruit", "seed",
      "light", "dark", "warm", "cold", "loud", "quiet", "fast", "slow", "good",
      "bad", "new", "old", "big", "small", "happy", "sad", "love", "hate"
    ];
  
    const randomWords = [];
    for (let i = 0; i < count; i++) {
      const randomIndex = Math.floor(Math.random() * words.length);
      randomWords.push(words[randomIndex]);
    }
    return randomWords;
  }



// frappe.call({
    //     method: "set_vendor_name",
    //     doc: frm.doc,
    //     callback:(r=>{
            
    //     })
    // })
