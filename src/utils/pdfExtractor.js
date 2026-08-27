/**
 * Lazy PDF parser loader to keep initial page load instantaneous
 */
let pdfjsPromise = null;

async function getPdfJs() {
  if (!pdfjsPromise) {
    pdfjsPromise = (async () => {
      const pdfjsLib = await import('pdfjs-dist');
      try {
        const workerModule = await import('pdfjs-dist/build/pdf.worker.min.mjs?url');
        pdfjsLib.GlobalWorkerOptions.workerSrc = workerModule.default || workerModule;
      } catch {
        pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjsLib.version || '4.10.38'}/build/pdf.worker.min.mjs`;
      }
      return pdfjsLib;
    })();
  }
  return pdfjsPromise;
}

/**
 * Extracts raw text from a PDF file lazily using pdfjs-dist with secondary stream fallback
 */
export async function extractTextFromPDF(file) {
  try {
    const arrayBuffer = await file.arrayBuffer();
    const pdfjsLib = await getPdfJs();

    const loadingTask = pdfjsLib.getDocument({
      data: new Uint8Array(arrayBuffer),
      useSystemFonts: true,
      disableFontFace: true,
      isEvalSupported: false,
    });

    const pdfDocument = await loadingTask.promise;
    const numPages = Math.min(pdfDocument.numPages, 30); // Cap at 30 pages for lightning speed
    let fullText = '';

    for (let pageNum = 1; pageNum <= numPages; pageNum++) {
      try {
        const page = await pdfDocument.getPage(pageNum);
        const textContent = await page.getTextContent();
        
        let lastY = null;
        let pageStr = '';
        
        for (const item of textContent.items) {
          if ('str' in item) {
            if (lastY !== null && Math.abs(item.transform[5] - lastY) > 6) {
              pageStr += '\n';
            } else if (pageStr.length > 0 && !pageStr.endsWith(' ') && !pageStr.endsWith('\n')) {
              pageStr += ' ';
            }
            pageStr += item.str;
            lastY = item.transform[5];
          }
        }

        const cleanPageStr = pageStr.trim();
        if (cleanPageStr) {
          fullText += cleanPageStr + '\n\n';
        }
      } catch (pageErr) {
        console.warn(`Error reading PDF page ${pageNum}:`, pageErr);
      }
    }

    if (fullText.trim().length > 20) {
      return fullText.trim();
    }
  } catch (pdfErr) {
    console.warn("Primary pdfjs extraction encountered error, attempting fallback:", pdfErr);
  }

  // Fast Fallback: parse printable text segments if pdfjs had issues
  try {
    const text = await file.text();
    const printable = text.replace(/[^\x20-\x7E\n\r\t]/g, ' ');
    const lines = printable
      .split('\n')
      .map(l => l.trim())
      .filter(l => l.length > 10 && !l.includes('obj') && !l.includes('endobj') && !l.includes('stream') && !l.includes('xref'));
    if (lines.length > 3) {
      return lines.join('\n');
    }
  } catch (e) {
    console.warn("Raw fallback also failed:", e);
  }

  return "";
}

/**
 * Main parser for user-uploaded syllabus documents (PDF, TXT, MD, DOCX, CSV)
 */
export async function parseUploadedDocument(file) {
  const fileName = file.name || "Uploaded_Document";
  const fileExt = fileName.split('.').pop()?.toLowerCase();

  let rawText = "";

  if (fileExt === 'pdf') {
    rawText = await extractTextFromPDF(file);
  } else if (fileExt === 'txt' || fileExt === 'md' || fileExt === 'json' || fileExt === 'csv') {
    rawText = await file.text();
  } else {
    try {
      rawText = await file.text();
    } catch {
      rawText = "";
    }
  }

  const cleanedText = (rawText || "").trim();
  return structureSyllabusContent(fileName, cleanedText);
}

/**
 * Intelligently extracts topics, units, and learning tasks from parsed document text
 */
export function structureSyllabusContent(fileName, rawText) {
  const baseTitle = fileName
    .replace(/\.[^/.]+$/, "")
    .replace(/[-_]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  // Split into clean lines
  const lines = rawText
    .split(/\r?\n/)
    .map(l => l.trim())
    .filter(l => l.length > 3 && !/^---\s*Page\s*\d+\s*---$/i.test(l));

  // Extract explicit Unit / Module / Chapter headings
  const modulePatterns = [
    /^(?:unit|module|chapter|week|phase|section|part)\s*[-:]?\s*([0-9ivxlcdm]+|[a-z])\s*[-:]?\s*(.*)$/i,
    /^(?:[0-9ivxlcdm]+|[a-z])[.)]\s+([a-zA-Z].*)$/i,
    /^#+\s+(.*)$/
  ];

  const detectedSections = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Check if line matches a syllabus header
    let matchedTitle = null;
    for (const pat of modulePatterns) {
      const match = line.match(pat);
      if (match) {
        matchedTitle = line.replace(/^[#*\-•\d.:)\s]+/, '').trim();
        if (matchedTitle.length < 3) matchedTitle = line;
        break;
      }
    }

    // Also check for ALL-CAPS topic titles (length 4 to 60)
    if (!matchedTitle && line.length >= 5 && line.length <= 65 && line === line.toUpperCase() && /[A-Z]/.test(line) && !line.includes('PAGE')) {
      matchedTitle = line;
    }

    if (matchedTitle && matchedTitle.length >= 4 && matchedTitle.length <= 90) {
      // Gather subtopics/lines under this section
      const subtopics = [];
      for (let j = i + 1; j < Math.min(i + 8, lines.length); j++) {
        const nextLine = lines[j];
        if (modulePatterns.some(p => p.test(nextLine))) break;
        if (nextLine.length >= 6 && nextLine.length <= 100) {
          subtopics.push(nextLine.replace(/^[•\-*\d.)\s]+/, '').trim());
        }
      }

      detectedSections.push({
        title: matchedTitle,
        subtopics: subtopics.slice(0, 4)
      });
      i += Math.min(subtopics.length, 3);
    }
  }

  // Deduplicate and filter section titles
  const uniqueSections = [];
  const seen = new Set();
  for (const s of detectedSections) {
    const norm = s.title.toLowerCase().replace(/[^a-z0-9]/g, '');
    if (norm.length > 3 && !seen.has(norm)) {
      seen.add(norm);
      uniqueSections.push(s);
    }
  }

  // Extract key concept phrases & topics across the text
  const extractedTopics = [];
  const topicCandidates = [
    ...uniqueSections.map(s => s.title),
    ...uniqueSections.flatMap(s => s.subtopics)
  ];

  // If we found specific section headers from the PDF
  for (const item of topicCandidates) {
    const clean = item.replace(/^(unit|module|chapter|week|topic)\s*\d+[:\-.]*\s*/i, '').trim();
    if (clean.length > 3 && clean.length < 70 && !extractedTopics.includes(clean)) {
      extractedTopics.push(clean);
    }
    if (extractedTopics.length >= 8) break;
  }

  // If few section headings were found, extract meaningful lines/phrases from the document
  if (extractedTopics.length < 4 && lines.length > 0) {
    for (const line of lines) {
      const parts = line.split(/[,;:•|\-/]/).map(p => p.trim()).filter(p => p.length >= 6 && p.length <= 60);
      for (const p of parts) {
        if (!extractedTopics.includes(p) && !p.toLowerCase().includes('syllabus') && !p.toLowerCase().includes('university') && !p.toLowerCase().includes('semester')) {
          extractedTopics.push(p);
        }
        if (extractedTopics.length >= 8) break;
      }
      if (extractedTopics.length >= 8) break;
    }
  }

  // Ensure fallback meaningful topics if document was extremely short
  if (extractedTopics.length === 0) {
    extractedTopics.push(
      `${baseTitle} Core Architecture & Principles`,
      `${baseTitle} Formulas, Theories & Mechanisms`,
      `${baseTitle} Experimental Methods & Applications`,
      `${baseTitle} Advanced Problem-Solving & Case Studies`
    );
  }

  // Generate 4-Phase Study Checklist with real extracted topics
  let modules = [];
  if (uniqueSections.length >= 3) {
    modules = uniqueSections.slice(0, 4).map((sec, idx) => {
      const t1 = sec.subtopics[0] || `Core theorems, definitions & principles of ${sec.title}`;
      const t2 = sec.subtopics[1] || `Detailed derivations, formulas & problem solving in ${sec.title}`;
      const t3 = sec.subtopics[2] || `Active recall exercises & mock quiz for Unit ${idx + 1}`;

      return {
        week: idx + 1,
        title: `Phase ${idx + 1}: ${sec.title}`,
        hours: `${8 + idx * 2} Hours`,
        tasks: [
          { id: `mod-${idx}-1`, title: `Study: ${t1}`, xp: 25 },
          { id: `mod-${idx}-2`, title: `Solve: ${t2}`, xp: 25 },
          { id: `mod-${idx}-3`, title: `Reinforce: ${t3}`, xp: 25 }
        ]
      };
    });
  } else {
    // Distribute extracted topics across 4 structured phases
    const t0 = extractedTopics[0] || `${baseTitle} Foundations`;
    const t1 = extractedTopics[1] || `${baseTitle} Core Dynamics`;
    const t2 = extractedTopics[2] || `${baseTitle} Advanced Mechanisms`;
    const t3 = extractedTopics[3] || `${baseTitle} Applied Systems`;

    modules = [
      {
        week: 1,
        title: `Phase 1: Foundations & Fundamentals (${t0})`,
        hours: "8 Hours",
        tasks: [
          { id: 'gen-1-1', title: `Review fundamental concepts & definitions in ${t0}`, xp: 25 },
          { id: 'gen-1-2', title: `Construct mental models & ELI10 analogies for ${t0}`, xp: 25 },
          { id: 'gen-1-3', title: `Solve 5 fundamental active recall diagnostic questions`, xp: 25 }
        ]
      },
      {
        week: 2,
        title: `Phase 2: Core Mechanisms & Analysis (${t1})`,
        hours: "10 Hours",
        tasks: [
          { id: 'gen-2-1', title: `Master key principles, formulas and structures in ${t1}`, xp: 25 },
          { id: 'gen-2-2', title: `Derive equations & analyze boundary conditions for ${t1}`, xp: 25 },
          { id: 'gen-2-3', title: `Execute 3 practical problem-solving worksheets`, xp: 25 }
        ]
      },
      {
        week: 3,
        title: `Phase 3: Advanced Topics & Integration (${t2})`,
        hours: "12 Hours",
        tasks: [
          { id: 'gen-3-1', title: `Deep dive into advanced syllabus theorems in ${t2}`, xp: 25 },
          { id: 'gen-3-2', title: `Implement real-world case study application for ${t2}`, xp: 25 },
          { id: 'gen-3-3', title: `Perform peer review & doubt resolution on ${baseTitle}`, xp: 25 }
        ]
      },
      {
        week: 4,
        title: `Phase 4: Synthesis, Kahoot Arena & Exam Readiness (${t3})`,
        hours: "14 Hours",
        tasks: [
          { id: 'gen-4-1', title: `Master comprehensive exam concepts for ${t3}`, xp: 50 },
          { id: 'gen-4-2', title: `Complete timed Kahoot mock test on ${baseTitle} with combo multiplier`, xp: 50 },
          { id: 'gen-4-3', title: `Review final high-yield formula cheat sheet & syllabus summary`, xp: 50 }
        ]
      }
    ];
  }

  // Create document summary snippet from actual text
  const cleanSnippet = rawText.length > 20
    ? rawText.slice(0, 320).replace(/\s+/g, ' ') + '...'
    : `Parsed syllabus for ${baseTitle}.`;

  // Dynamically generate Quiz questions grounded in the extracted topics
  const generatedQuizQuestions = generateDynamicQuiz(baseTitle, extractedTopics);

  return {
    fileName,
    title: baseTitle,
    rawText: rawText.slice(0, 15000),
    totalChunks: Math.max(12, Math.floor(rawText.length / 150) || 24),
    modules,
    extractedTopics: extractedTopics.slice(0, 6),
    extractedSnippet: cleanSnippet,
    quizQuestions: generatedQuizQuestions
  };
}

/**
 * Generates dynamic 4-choice Kahoot-style quiz questions grounded in the extracted syllabus
 */
function generateDynamicQuiz(title, topics) {
  const t0 = topics[0] || `${title} Fundamentals`;
  const t1 = topics[1] || `${title} Dynamics`;
  const t2 = topics[2] || `${title} Advanced Analysis`;

  return [
    {
      id: 1,
      topic: `${title}: ${t0}`,
      question: `What is the primary governing principle behind ${t0}?`,
      options: [
        `Systematic decomposition and invariant conservation laws governing ${t0}`,
        `Random distribution with arbitrary non-deterministic state shifts`,
        `Direct brute-force enumeration without structural constraints`,
        `External compilation bypassing all fundamental axioms`
      ],
      correctIndex: 0,
      eli10: `Think of ${t0} like the foundation blocks of a house. Everything stays strong and balanced because each part follows strict, predictable rules!`,
      points: 1000
    },
    {
      id: 2,
      topic: `${title}: ${t1}`,
      question: `In the context of ${title}, how is ${t1} most effectively analyzed?`,
      options: [
        `By ignoring boundary constraints and assuming uniform zero entropy`,
        `By evaluating state transitions, rate laws, and energy/information exchange`,
        `By restricting observation to single isolated static points`,
        `By replacing mathematical models with random simulations`
      ],
      correctIndex: 1,
      eli10: `Imagine ${t1} like tracking cars on a highway. You don't just look at one parked car; you measure the speed, flow, and how they interact!`,
      points: 1200
    },
    {
      id: 3,
      topic: `${title}: ${t2}`,
      question: `What critical trade-off or advantage occurs when implementing ${t2}?`,
      options: [
        `Decreased precision with exponential latency overhead`,
        `Enhanced stability and optimized throughput within defined operating limits`,
        `Complete elimination of all physical and computational bounds`,
        `Zero energy consumption with infinite scalability`
      ],
      correctIndex: 1,
      eli10: `Like upgrading from a bicycle to a high-speed train: you get much faster and carry more, but you need smooth tracks and careful scheduling!`,
      points: 1100
    }
  ];
}
