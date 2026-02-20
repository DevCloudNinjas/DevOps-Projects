const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const green = '\x1b[32m';
const reset = '\x1b[0m';
const yellow = '\x1b[33m';
const red = '\x1b[31m';
const MASTER_RECORD_PATH = path.join(__dirname, '../docs/README.md');
const SIDEBAR_PATH = path.join(__dirname, '../docs/_sidebar.md');

async function main() {
    try {

        // See if we should update the master record
        const args = process.argv.slice(2);
        let update = false;
        if (args[0] === 'update') {
            update = true;
        }

        // Using _sidebar.md as the list of exercises that we cover in the bootcamp
        // create a list of all markdown files that might contain front-matter
        const sidebar = fs.readFileSync(SIDEBAR_PATH, 'utf8');

        const markdownFiles = sidebar.match(/\([^\)]+\.md\)/g);

        // Remove parentheses and filter out addendum items
        const cleanedFiles = markdownFiles
            .map(file => file.slice(1, -1))
            .filter(file => !file.startsWith('addendum'))
            .map(file => path.join(__dirname, '../docs/',  file ));

        // Read the master record and extract just the front matter.
        let { data: masterRecord, content } = matter(fs.readFileSync(MASTER_RECORD_PATH, 'utf8'));

        // Object where we will rebuild the master record
        let data = {};

        let masterRecordChanged = false;

        for (const mdFile of cleanedFiles) {
            if (!fs.existsSync(mdFile)) {
                console.error(`${red}${mdFile} does not exist or _sidebar.md needs to be udpated.${reset}`);
                process.exit(1);
            }

            // Read the content of the .md file.
            const fileContent = fs.readFileSync(mdFile, 'utf8');

            // Parse the YAML front matter.
            const { data: exerciseData } = matter(fileContent);

            // merge the front-matter from the staged file into the master record.
            // This will overwrite the inner object on the master record if it exists
            // and also add it if it doesnt.
            if (exerciseData) {
                data = { ...data, ...exerciseData };
                masterRecordChanged = true;
            }
        }

        // Create an array of key-value pairs and then sorts them alphabetically by the keys.
        const sortedEntries = Object.entries(data).sort(
            (a, b) => a[0].localeCompare(b[0])
        );
        const sortedMasterEntries = Object.entries(masterRecord).sort(
            (a, b) => a[0].localeCompare(b[0])
        );

        // Create a new object from the sorted entries
        const sortedData = Object.fromEntries(sortedEntries);
        const sortedMasterRecord = Object.fromEntries(sortedMasterEntries);

        // Stringify the object and compare. This handles the case of an .md file being updated
        // but not the front-data
        if (JSON.stringify(sortedData) === JSON.stringify(sortedMasterRecord)) {
            masterRecordChanged = false;
        }

        if (masterRecordChanged) {
            // Stringify the updated front-matter and origional content
            const updatedContent = matter.stringify(content, sortedData);

            // Update the master record with the new front-matter. Use the sorted
            if (update) {
                fs.writeFileSync(MASTER_RECORD_PATH, updatedContent);
                console.error(`${yellow}New front matter detected${reset}`);
                console.error(`${yellow}Please review changes to ./docs/README.md${reset}`);
                process.exit(1);
            }
            console.error(`${yellow}Front matter missing from master record. Locally run \`npm run refresh-front-matter\`${reset}`);
            process.exit(1);
        } else {
            // Continue with the commit.
            console.log(`${green}No changes to master record, proceeding with commit.${reset}`);
            process.exit(0);
        }

    } catch (error) {
        console.error('An error occurred:', error);
        process.exit(1);
    }
}

main();
